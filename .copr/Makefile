# COPR make-srpm entry point. Both packages use the same pinned Omadora commit.

spec ?= packaging/rpm/omarchy/omarchy.spec
outdir ?= $(CURDIR)/srpm

.PHONY: srpm
srpm:
	@set -e; \
	case '$(spec)' in \
	  packaging/rpm/omarchy/omarchy.spec|packaging/rpm/omarchy-settings/omarchy-settings.spec) ;; \
	  *) echo 'Unknown Omadora package spec: $(spec)' >&2; exit 1 ;; \
	esac; \
	source=$${OMADORA_SOURCE:-}; \
	if [ -z "$$source" ]; then \
	  source=$$(mktemp -d); \
	  trap 'rm -rf "$$source"' EXIT; \
	  git clone --filter=blob:none --no-checkout https://github.com/kamm3r/omadora.git "$$source"; \
	  git -C "$$source" checkout "$$(cat "$(CURDIR)/omadora-revision")"; \
	fi; \
	if [ "$$(git -C "$$source" rev-parse HEAD)" != "$$(cat "$(CURDIR)/omadora-revision")" ]; then \
	  echo 'Omadora source does not match omadora-revision' >&2; exit 1; \
	fi; \
	$(MAKE) -C "$$source" -f .copr/Makefile srpm outdir='$(abspath $(outdir))' spec='$(spec)'
