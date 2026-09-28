# COPR make-srpm entry point for the pinned Omadora pair and local RPM recipes.

spec ?= packaging/rpm/omarchy/omarchy.spec
outdir ?= $(CURDIR)/srpm

.PHONY: srpm
srpm:
	@set -e; \
	command -v git >/dev/null || dnf -y install git; \
	spec='$(spec)'; \
	case "$$spec" in \
	  */omarchy/omarchy.spec | */omarchy-settings/omarchy-settings.spec) \
	    $(MAKE) -f '$(CURDIR)/.copr/core.mk' srpm outdir='$(abspath $(outdir))' spec="$$spec"; \
	    exit 0 ;; \
	  packages/*/*.spec | */packages/*/*.spec) \
	    name=$$(basename "$$spec" .spec); \
	    recipe="$(CURDIR)/packages/$$name/$$name.spec"; \
	    checksum="$(CURDIR)/packages/$$name/sources.sha256"; \
	    if [ ! -f "$$recipe" ] || [ ! -f "$$checksum" ]; then \
	      echo "Unknown Omadora package spec: $$spec" >&2; exit 1; \
	    fi; \
	    command -v spectool >/dev/null && command -v rpmbuild >/dev/null || dnf -y install rpmdevtools rpm-build; \
	    mkdir -p '$(outdir)'; \
	    cp "$$recipe" '$(outdir)/'; \
	    spectool -g -C '$(outdir)' "$(outdir)/$$name.spec"; \
	    (cd '$(outdir)' && sha256sum -c "$$checksum"); \
	    if [ -f "$(CURDIR)/packages/$$name/cargo-vendor" ]; then \
	      command -v cargo >/dev/null || dnf -y install cargo; \
	      version=$$(rpmspec -q --srpm --qf '%{VERSION}' "$$recipe"); \
	      vendor_tmp=$$(mktemp -d); \
	      trap 'rm -rf "$$vendor_tmp"' EXIT; \
	      tar -xzf "$(outdir)/$$name-$$version.tar.gz" -C "$$vendor_tmp"; \
	      (cd "$$vendor_tmp/$$name-$$version" && \
	        mkdir -p .cargo && \
	        cargo vendor --locked --versioned-dirs vendor >.cargo/config.toml && \
	        tar -czf "$(abspath $(outdir))/$$name-vendor-$$version.tar.gz" vendor .cargo); \
	    fi; \
	    rpmbuild -bs --define '_sourcedir $(abspath $(outdir))' --define '_srcrpmdir $(abspath $(outdir))' "$(outdir)/$$name.spec"; \
	    exit 0 ;; \
	  *) echo "Unknown Omadora package spec: $$spec" >&2; exit 1 ;; \
	esac; \
	:
