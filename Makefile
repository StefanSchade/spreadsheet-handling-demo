# =========================
# User Config
# =========================

LIB_SRC ?= ../core
LIB_PYPI_VERSION ?= 0.1.0b6

# =========================
# Virtualenv / Python
# =========================
SHELL 		 := /usr/bin/env bash
.SHELLFLAGS  := -eu -o pipefail -c

VENV         ?= .venv
PYTHON       := $(VENV)/bin/python

# =========================
# Paths and Naming
# =========================
ROOT         ?= $(CURDIR)/
TMP_DIR      ?= ./tmp
BUILD_DIR    ?= ./target

# =========================
# Stamps (avoid repeated installs on WSL)
# =========================
STAMP_DIR    ?= .stamps
STAMP_SETUP  := $(STAMP_DIR)/setup.ok
STAMP_VENV   := $(STAMP_DIR)/venv.ok

# =========================
# CLI bindings (venv executables)
# =========================
RUN_CMD      := $(VENV)/bin/sheets-run

# =========================
# Environment & dependencies
# =========================
.PHONY: setup reset-deps venv

# One-time venv creation (stamped)
$(STAMP_VENV):
	@test -d "$(VENV)" || python3 -m venv "$(VENV)"
	@mkdir -p "$(STAMP_DIR)"
	@touch "$(STAMP_VENV)"

# Install project (pyproject.toml) into .venv (dev extras), stamped to suppress WSL timestamp churn
$(STAMP_SETUP): pyproject.toml | $(STAMP_VENV) $(STAMP_DIR)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"
	@touch "$(STAMP_SETUP)"

setup: $(STAMP_SETUP) ## Create venv (if missing) and install deps once (uses stamps)

reset-deps: ## Remove venv and stamps (forces a fresh setup next time)
	rm -rf "$(VENV)" "$(STAMP_DIR)"

# Keep a legacy alias if someone runs `make deps` out of habit
.PHONY: deps
deps: setup

# =========================
# Targets
# =========================

.PHONY: run
run: ## Execute a checked-in run config / pipeline (preferred demo entry point)
	@set -e; \
	if [[ -z "$(PIPELINE)" ]]; then \
		echo "❌ No PIPELINE provided. Usage: make run PIPELINE=./pipelines/demo_*.yaml"; exit 2; \
	fi; \
	if [[ ! -f "$(PIPELINE)" ]]; then \
		echo "❌ Pipeline file not found: $(PIPELINE)"; exit 2; \
	fi; \
	echo "Running pipeline config: $(PIPELINE)"; \
	$(RUN_CMD) \
	  --config "$(PIPELINE)" \
	  $(if $(IN_KIND),--in-kind '$(IN_KIND)') \
	  $(if $(IN_PATH),--in-path '$(IN_PATH)') \
	  $(if $(OUT_KIND),--out-kind '$(OUT_KIND)') \
	  $(if $(OUT_PATH),--out-path '$(OUT_PATH)')

.PHONY: lint-json
lint-json:
	@command -v jq >/dev/null || { echo "Install jq"; exit 2; }
	@find data -name '*.json' -print -exec sh -c 'jq . "{}" >/dev/null || echo "Invalid: {}"' \;

# =========================
# Switch local and pip lib
# =========================
.PHONY: setup-lib-local
setup-lib-local: ## Use local spreadsheet-handling from a sibling checkout (override with LIB_SRC=...)
	@test -d "$(VENV)" || python3 -m venv "$(VENV)"
	$(PYTHON) -m pip uninstall -y spreadsheet-handling || true
	$(PYTHON) -m pip install -e '$(LIB_SRC)'
	@echo "OK: using local spreadsheet-handling from $(LIB_SRC)"

.PHONY: setup-lib-pypi
setup-lib-pypi: ## Switch back to pinned PyPI version
	@test -d "$(VENV)" || python3 -m venv "$(VENV)"
	$(PYTHON) -m pip uninstall -y spreadsheet-handling || true
	$(PYTHON) -m pip install 'spreadsheet-handling==$(LIB_PYPI_VERSION)'
	@echo "OK: using PyPI spreadsheet-handling $(LIB_PYPI_VERSION)"

.PHONY: snapshot
snapshot: ## Optional: repo snapshot (script is not part of this demo repository)
	@mkdir -p "$(BUILD_DIR)"
	@if [ -x "$(ROOT)tools/repo_snapshot.sh" ]; then \
	  "$(ROOT)tools/repo_snapshot.sh" "$(ROOT)" "$(BUILD_DIR)" "$(BUILD_DIR)/spreadsheet-handling-demo.txt"; \
	else \
	  echo "⚠️  script not found: $(ROOT)tools/repo_snapshot.sh"; \
	  echo "⚠️  not committed to this repo since non-essential for the demo"; \
	  echo "⚠️  manually copy if needed from: https://github.com/StefanSchade/spreadsheet-handling/tree/main/tools"; \
	fi

.PHONY: render-slides
render-slides: ## Render AsciiDoc walkthroughs to Reveal.js HTML under build/slides/
	@bash scripts/render_slides.sh

.PHONY: clean
clean: ## Remove tmp and target
	rm -rf "$(TMP_DIR)" "$(BUILD_DIR)"

$(STAMP_DIR):
	@mkdir -p "$(STAMP_DIR)"

.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "};{printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
