Name:           ttf-jetbrains-mono-nerd-basic
Version:        3.5.1
Release:        1%{?dist}
Summary:        Basic JetBrains Mono Nerd Font family
License:        OFL-1.1-no-RFN
URL:            https://github.com/ryanoasis/nerd-fonts
Source0:        %{url}/releases/download/v%{version}/JetBrainsMono.zip#/JetBrainsMono-%{version}.zip
BuildArch:      noarch
BuildRequires:  unzip
Provides:       ttf-font-nerd

%description
Regular, Bold, Italic, and Bold Italic faces of the JetBrains Mono Nerd Font.

%prep
%setup -q -c -T
unzip -q %{SOURCE0} JetBrainsMonoNerdFont-Regular.ttf JetBrainsMonoNerdFont-Bold.ttf JetBrainsMonoNerdFont-Italic.ttf JetBrainsMonoNerdFont-BoldItalic.ttf OFL.txt

%build

%install
install -d %{buildroot}%{_datadir}/fonts/%{name}
install -m 0644 JetBrainsMonoNerdFont-{Regular,Bold,Italic,BoldItalic}.ttf %{buildroot}%{_datadir}/fonts/%{name}/

%files
%license OFL.txt
%{_datadir}/fonts/%{name}

%changelog
* Mon Sep 28 2026 kamm3r - 3.5.1-1
- Port the upstream Omarchy font package to Fedora.
