# Build the two Omadora source packages from one pinned source commit. The
# specs live here under packaging/rpm/; the source is the Omadora commit named
# in omadora-revision, so both packages carry exactly the same tree.

.PHONY: srpm
srpm:
	@set -e; \
	spec='$(spec)'; \
	case "$$spec" in \
	  */omarchy/omarchy.spec) name=omarchy ;; \
	  */omarchy-settings/omarchy-settings.spec) name=omarchy-settings ;; \
	  *) echo "Unknown core spec: $$spec" >&2; exit 1 ;; \
	esac; \
	command -v rpmbuild >/dev/null && command -v git >/dev/null || dnf -y install git rpm-build; \
	revision=$$(cat '$(CURDIR)/omadora-revision'); \
	source=$${OMADORA_SOURCE:-}; \
	if [ -z "$$source" ]; then \
	  source=$$(mktemp -d); \
	  trap 'rm -rf "$$source"' EXIT; \
	  git clone --filter=blob:none --no-checkout https://github.com/kamm3r/omadora.git "$$source"; \
	fi; \
	git() { command git -c safe.directory="$$source" "$$@"; }; \
	if ! git -C "$$source" cat-file -e "$$revision^{commit}" 2>/dev/null; then \
	  echo "Omadora source does not contain omadora-revision $$revision" >&2; exit 1; \
	fi; \
	version=$$(git -C "$$source" show "$$revision:version" | sed -E 's/[.-]([a-z])/~\1/'); \
	commits=$$(git -C "$$source" rev-list --count "$$revision"); \
	sha=$$(git -C "$$source" rev-parse --short=10 "$$revision"); \
	release=0.$$commits.git$$sha; \
	mkdir -p '$(abspath $(outdir))'; \
	git -C "$$source" archive --format=tar.gz --prefix="omarchy-$$version/" -o '$(abspath $(outdir))'/"omarchy-$$version.tar.gz" "$$revision"; \
	{ printf '%%global omarchy_version %s\n%%global omarchy_release %s\n' "$$version" "$$release"; cat '$(CURDIR)'/packaging/rpm/"$$name/$$name.spec"; } >'$(abspath $(outdir))'/"$$name.spec"; \
	rpmbuild -bs --define '_sourcedir $(abspath $(outdir))' --define '_srcrpmdir $(abspath $(outdir))' '$(abspath $(outdir))'/"$$name.spec"
