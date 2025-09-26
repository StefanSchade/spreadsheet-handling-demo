# =========================
# User Config
# =========================

CONFIG := sheets.yaml

# =========================
# Virtualenv / Python
# =========================
SHELL        := /usr/bin/env bash -eo pipefail

VENV         ?= .venv
PYTHON       := $(VENV)/bin/python

# =========================
# Paths & Naming
# =========================
ROOT         ?= $(CURDIR)/
DATA_DIR     ?= ./data
TMP_DIR      ?= ./tmp
BUILD_DIR    ?= ./target
SHA          ?= $(shell git rev-parse --short HEAD)

# All top-level data sets (each dir under ./data becomes one workbook)
PACK_SETS    := $(shell find $(DATA_DIR) -maxdepth 1 -mindepth 1 -type d -printf "%f\n")

# =========================
# Stamps (avoid repeated installs on WSL)
# =========================
STAMP_DIR    ?= .stamps
STAMP_SETUP  := $(STAMP_DIR)/setup.ok
STAMP_VENV   := $(STAMP_DIR)/venv.ok

# =========================
# CLI bindings (venv executables)
# =========================
PACK_CMD     := $(VENV)/bin/sheets-pack
UNPACK_CMD   := $(VENV)/bin/sheets-unpack
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
	$(PYTHON) -m pip install -e '.[dev]'
	@touch "$(STAMP_SETUP)"

setup: $(STAMP_SETUP) ## Create venv (if missing) and install deps once (uses stamps)

reset-deps: ## Remove venv and stamps (forces a fresh setup next time)
	rm -rf "$(VENV)" "$(STAMP_DIR)"

# Keep a legacy alias if someone runs `make deps` out of habit
.PHONY: deps
deps: setup

# =========================
# Targets (no implicit deps -> quick roundtrip)
# =========================

.PHONY: pack
pack: ## JSON -> XLSX for every dataset under ./data (run `make setup` once before)
	@mkdir -p "$(TMP_DIR)"
	@for d in $(PACK_SETS); do \
		out="$(TMP_DIR)/$${d}-$(SHA).xlsx"; \
		echo "Packing $(DATA_DIR)/$$d -> $$out"; \
		$(PACK_CMD) "$(DATA_DIR)/$$d" -o "$$out"; \
	done
	@echo "OK: workbooks in $(TMP_DIR)"

.PHONY: unpack
unpack: ## XLSX -> JSON roundtrip back into ./data (skip Excel lock files)
	@set -e; \
	shopt -s nullglob; \
	for x in $(TMP_DIR)/*.xlsx; do \
		base=$$(basename "$$x"); \
		# Skip Excel lock/temp files like "~$foo.xlsx"
		if [[ "$$base" == '~$'* ]]; then \
			echo "Skipping Excel lock file: $$x"; \
			continue; \
		fi; \
		name_noext=$${base%.xlsx}; \
		set=$${name_noext%-$(SHA)}; \
		echo "Unpacking $$x -> $(DATA_DIR)/$$set"; \
		$(UNPACK_CMD) "$$x" -o "$(DATA_DIR)/$$set"; \
	done
	@echo "OK: JSON updated under $(DATA_DIR)"

.PHONY: roundtrip
roundtrip: pack unpack ## Convenience: pack + unpack

.PHONY: verify
verify: ## Run verification pipeline via sheets-run (json_dir -> xlsx)
	$(RUN_CMD) \
	  --config "$(CONFIG)" \
	  --pipeline verify \
	  --in-kind json_dir  --in-path "$(DATA_DIR)" \
	  --out-kind xlsx     --out-path "$(TMP_DIR)/_verify-$(SHA).xlsx"
	@echo "OK: verification"

.PHONY: extract
extract: ## Run extract pipeline via sheets-run (json_dir -> json_dir)
	@mkdir -p "$(BUILD_DIR)"
	$(RUN_CMD) \
	  --config "$(CONFIG)" \
	  --pipeline extract \
	  --in-kind json_dir  --in-path "$(DATA_DIR)" \
	  --out-kind json_dir --out-path "$(BUILD_DIR)"
	@echo "OK: artifacts in $(BUILD_DIR)"

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
	$(PYTHON) -m pip install 'spreadsheet-handling==0.1.0b2'
	@echo "OK: using PyPI spreadsheet-handling 0.1.0b2"

.PHONY: snapshot
snapshot: ## Optional: repo snapshot (script is not part of this demo repository)
	@mkdir -p "$(BUILD_DIR)"
	@if [ -x "$(ROOT)tools/repo_snapshot.sh" ]; then \
	  "$(ROOT)tools/repo_snapshot.sh" "$(ROOT)" "$(BUILD_DIR)" "$(BUILD_DIR)/repo.txt"; \
	else \
	  echo "⚠️  script not found: $(ROOT)tools/repo_snapshot.sh"; \
	  echo "⚠️  not committed to this repo since non-essential for the demo"; \
	  echo "⚠️  manually copy if needed from: https://github.com/StefanSchade/spreadsheet-handling/tree/main/tools"; \
	fi

.PHONY: clean
clean: ## Remove tmp and target
	rm -rf "$(TMP_DIR)" "$(BUILD_DIR)"

$(STAMP_DIR):
	@mkdir -p "$(STAMP_DIR)"

.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "};{printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
