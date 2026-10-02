%global debug_package %{nil}
%global omarchy_pkgs_commit 29465fb750ed2b7a8b3f409cf1a61989ac2d3867

Name:           omarchy-nvim
Version:        2026.9.21
Release:        1%{?dist}
Summary:        Pre-built LazyVim configuration with cached plugins
License:        MIT
URL:            https://github.com/LazyVim/LazyVim
Source0:        https://github.com/LazyVim/starter/archive/refs/heads/main.tar.gz#/%{name}-starter-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-nvim/lazyvim.json
Source2:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-nvim/omarchy-nvim-setup
Source3:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-nvim/lua/config/options.lua
Source4:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-nvim/lua/config/remote_clipboard.lua
Source5:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-nvim/lua/plugins/all-themes.lua
Source6:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-nvim/lua/plugins/disable-news-alert.lua
Source7:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-nvim/lua/plugins/omarchy-theme-hotreload.lua
Source8:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-nvim/lua/plugins/snacks-animated-scrolling-off.lua
Source9:        https://raw.githubusercontent.com/omacom/omarchy-pkgs/%{omarchy_pkgs_commit}/pkgbuilds/omarchy-nvim/plugin/after/transparency.lua
BuildArch:      noarch
BuildRequires:  git
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  tree-sitter-cli
BuildRequires:  neovim
Requires:       neovim >= 0.9.0
Requires:       git
Requires:       xdg-utils

%description
Pre-built LazyVim configuration with cached plugins.

%prep
%autosetup -n starter-main

%build
slim_lazy_repos() {
  local data_dir="$1"
  local dir

  for dir in "$data_dir"/lazy/*/; do
    [[ -d "$dir/.git" ]] || continue

    # Exclude test suites via sparse-checkout rather than rm: the worktree
    # stays clean, so the restore pass in %%install does not resurrect them
    # and future :Lazy checkouts keep honoring the exclusion. snacks.nvim
    # alone ships 18 MB of tests.
    git -C "$dir" sparse-checkout set --no-cone '/*' '!/test/' '!/tests/' '!/spec/'

    # Cut history down to the checked-out tips: drop the refs that pin older
    # objects, mark every remaining tip as a shallow boundary, then gc. This
    # is half the package -- ~70 MB of .git across the plugins. `git fetch`
    # into a shallow repo stays shallow and re-fetches tags, so :Lazy update
    # still works.
    #
    # Keep refs/remotes/origin/HEAD. It pins no objects (it is a symref, and
    # stays readable after its target ref is gone), but lazy.nvim resolves the
    # default branch through it for plugins parked on a detached HEAD by a
    # version pin -- lazy.nvim, LazyVim and blink.cmp. Without it, get_branch()
    # returns nil and every lockfile write asserts, so :Lazy install/update/sync
    # dies with E5113 on a fresh install.
    git -C "$dir" for-each-ref --format='%%(refname)' refs/remotes refs/tags |
      while IFS= read -r ref; do
        [[ $ref == refs/remotes/origin/HEAD ]] && continue
        git -C "$dir" update-ref -d "$ref"
      done
    rm -f "$dir/.git/FETCH_HEAD" "$dir/.git/ORIG_HEAD"
    {
      git -C "$dir" rev-parse HEAD
      git -C "$dir" for-each-ref --format='%%(objectname)' refs/heads
    } | sort -u >"$dir/.git/shallow"
    git -C "$dir" reflog expire --expire=all --all

    # lazy.nvim clones with --filter=blob:none, which marks the pack as a
    # promisor pack that gc refuses to repack or prune. The repo is shallow
    # at its tips now, so everything reachable exists locally: drop the
    # promisor markers and the stale commit-graph, then gc for real. Future
    # fetches simply run unfiltered.
    git -C "$dir" config --unset-all remote.origin.promisor || true
    git -C "$dir" config --unset-all remote.origin.partialclonefilter || true
    rm -f "$dir/.git/objects/pack/"*.promisor "$dir/.git/objects/info/commit-graph"
    rm -rf "$dir/.git/objects/info/commit-graphs"
    git -C "$dir" -c gc.writeCommitGraph=false gc --prune=now --quiet
  done
}

export HOME="%{_builddir}/nvim-build-home"
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_STATE_HOME="$HOME/.local/state"
export XDG_CACHE_HOME="$HOME/.cache"

mkdir -p "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" "$XDG_STATE_HOME" "$XDG_CACHE_HOME"

# Setup LazyVim starter
cp -a "%{_builddir}/starter-main" "$XDG_CONFIG_HOME/nvim"
rm -rf "$XDG_CONFIG_HOME/nvim/.git"

# Copy custom configs (mirrors PKGBUILD cp -r of startdir lua/plugin plus lazyvim.json)
mkdir -p "$XDG_CONFIG_HOME/nvim/lua/config" "$XDG_CONFIG_HOME/nvim/lua/plugins" "$XDG_CONFIG_HOME/nvim/plugin/after"
cp -a "%{SOURCE3}" "$XDG_CONFIG_HOME/nvim/lua/config/options.lua"
cp -a "%{SOURCE4}" "$XDG_CONFIG_HOME/nvim/lua/config/remote_clipboard.lua"
cp -a "%{SOURCE5}" "$XDG_CONFIG_HOME/nvim/lua/plugins/all-themes.lua"
cp -a "%{SOURCE6}" "$XDG_CONFIG_HOME/nvim/lua/plugins/disable-news-alert.lua"
cp -a "%{SOURCE7}" "$XDG_CONFIG_HOME/nvim/lua/plugins/omarchy-theme-hotreload.lua"
cp -a "%{SOURCE8}" "$XDG_CONFIG_HOME/nvim/lua/plugins/snacks-animated-scrolling-off.lua"
cp -a "%{SOURCE9}" "$XDG_CONFIG_HOME/nvim/plugin/after/transparency.lua"
cp -a "%{SOURCE1}" "$XDG_CONFIG_HOME/nvim/lazyvim.json"

echo "Installing LazyVim plugins..."
nvim --headless \
  "+Lazy! sync" \
  "+qa!" || true

echo "Slimming plugin repos..."
slim_lazy_repos "$XDG_DATA_HOME/nvim"

%install
restore_lazy_worktrees() {
  local data_dir="$1"
  local dir

  for dir in "$data_dir"/lazy/*/; do
    [[ -d "$dir/.git" ]] || continue
    git --git-dir="$dir/.git" --work-tree="$dir" restore .
  done
}

export HOME="%{_builddir}/nvim-build-home"
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"

install -dm755 %{buildroot}%{_datadir}/%{name}

cp -a "$XDG_CONFIG_HOME/nvim" %{buildroot}%{_datadir}/%{name}/config
cp -a "$XDG_DATA_HOME/nvim" %{buildroot}%{_datadir}/%{name}/data

# Remove everything from site/ directory but keep the directory to prevent error
rm -rf %{buildroot}%{_datadir}/%{name}/data/site/*
mkdir -p %{buildroot}%{_datadir}/%{name}/data/site

# Fix permissions to be readable by all users
chmod -R 755 %{buildroot}%{_datadir}/%{name}
find %{buildroot}%{_datadir}/%{name} -type f -exec chmod 644 {} \;

# Restore plugin worktree modes after the package-wide chmod so users seeded
# from /etc/skel do not need a first-login omarchy-nvim-setup cleanup pass.
restore_lazy_worktrees %{buildroot}%{_datadir}/%{name}/data

# Seed new users via /etc/skel. The installer installs omarchy-nvim before
# creating the first user, so this handles initial ISO installs and future
# users without an extra overwrite step.
install -dm755 %{buildroot}/etc/skel/.config %{buildroot}/etc/skel/.local/share
cp -a %{buildroot}%{_datadir}/%{name}/config %{buildroot}/etc/skel/.config/nvim
cp -a %{buildroot}%{_datadir}/%{name}/data %{buildroot}/etc/skel/.local/share/nvim
ln -snf "../../../../.local/state/omarchy/current/theme/neovim.lua" \
  %{buildroot}/etc/skel/.config/nvim/lua/plugins/theme.lua

# Ship the plugin cache once, now that /etc/skel has its copy. Keeping a
# second one under /usr/share made omarchy-nvim the largest package in an
# Omarchy install after noto-fonts-cjk — ~116 MiB installed, ~88 MB of it read
# off the ISO on every install. config/ stays: migrations read it from there.
rm -rf %{buildroot}%{_datadir}/%{name}/data

# Install setup/refresh commands to /usr/bin. setup fills missing pieces;
# refresh explicitly backs up and overwrites with the same /etc/skel defaults
# used for newly-created users.
install -Dm755 "%{SOURCE2}" %{buildroot}%{_bindir}/omarchy-nvim-setup
ln -s omarchy-nvim-setup %{buildroot}%{_bindir}/omarchy-nvim-refresh

%files
%license LICENSE
%{_datadir}/%{name}/config
%{_bindir}/omarchy-nvim-setup
%{_bindir}/omarchy-nvim-refresh
/etc/skel/.config/nvim
/etc/skel/.local/share/nvim

%changelog
* Wed Sep 30 2026 kamm3r - 2026.9.21-1
- Port the upstream Omarchy LazyVim recipe to Fedora.
