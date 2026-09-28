# Build the two Omadora source packages from one pinned source commit.

.PHONY: srpm
srpm:
	@set -e; \
	spec='$(spec)'; \
	case "$$spec" in \
	  */omarchy/omarchy.spec) spec=packaging/rpm/omarchy/omarchy.spec ;; \
	  */omarchy-settings/omarchy-settings.spec) spec=packaging/rpm/omarchy-settings/omarchy-settings.spec ;; \
	  *) echo "Unknown core spec: $$spec" >&2; exit 1 ;; \
	esac; \
	source=$${OMADORA_SOURCE:-}; \
	if [ -z "$$source" ]; then \
	  source=$$(mktemp -d); \
	  trap 'rm -rf "$$source"' EXIT; \
	  git clone --filter=blob:none --no-checkout https://github.com/kamm3r/omadora.git "$$source"; \
	  git -C "$$source" -c advice.detachedHead=false checkout "$$(cat "$(CURDIR)/omadora-revision")"; \
	fi; \
	if [ "$$(git -C "$$source" rev-parse HEAD)" != "$$(cat "$(CURDIR)/omadora-revision")" ]; then \
	  echo 'Omadora source does not match omadora-revision' >&2; exit 1; \
	fi; \
	$(MAKE) -C "$$source" -f .copr/Makefile srpm outdir='$(abspath $(outdir))' spec="$$spec"
