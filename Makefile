# =========================
# Virtualenv / Python
# =========================
SHELL := /usr/bin/env bash -eo pipefail

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
# Environment & dependencies
# =========================
.PHONEY: venv deps
venv: ## Create .venv if missing
	@test -d "$(VENV)" || python3 -m venv "$(VENV)"

deps: venv ## Install project (pyproject.toml) into .venv (dev extras included)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e '.[dev]'

# =========================
# CLI bindings (venv executables)
# =========================
PACK_CMD     := $(VENV)/bin/sheets-pack
UNPACK_CMD   := $(VENV)/bin/sheets-unpack
RUN_CMD      := $(VENV)/bin/sheets-run

# =========================
# Targets
# =========================
.PHONY: pack
pack: deps ## JSON -> XLSX for every dataset under ./data
	@mkdir -p "$(TMP_DIR)"
	@for d in $(PACK_SETS); do \
		out="$(TMP_DIR)/$${d}-$(SHA).xlsx"; \
		echo "Packing $(DATA_DIR)/$$d -> $$out"; \
		$(PACK_CMD) --input "$(DATA_DIR)/$$d" --output "$$out"; \
	done
	@echo "OK: workbooks in $(TMP_DIR)"

.PHONY: unpack
unpack: deps ## XLSX -> JSON roundtrip back into ./data (delete missing)
	@for x in $(TMP_DIR)/*.xlsx; do \
		base=$$(basename "$$x" .xlsx); set=$${base%-$(SHA)}; \
		echo "Unpacking $$x -> $(DATA_DIR)/$$set"; \
		$(UNPACK_CMD) --input "$$x" --output "$(DATA_DIR)/$$set" --delete-missing; \
	done
	@echo "OK: JSON updated under $(DATA_DIR)"

.PHONY: roundtrip
roundtrip: pack unpack ## Convenience: pack + unpack

.PHONY: verify
verify: deps ## Run verification pipeline (Frames->Frames step, 'warn' or 'fail' via profile/pipeline config)
	# Example uses 'verify' profile/pipeline; adjust if you rename in your repo
	$(RUN_CMD) --profile verify --pipeline verify --input "$(DATA_DIR)" --output "$(TMP_DIR)/_verify-$(SHA).xlsx"
	@echo "OK: verification"

.PHONY: extract
extract: deps ## Run extract pipeline (Frames->Frames), then persist via adapter into ./target
	@mkdir -p "$(BUILD_DIR)"
	# Example uses 'extract' profile/pipeline; adjust if you rename in your repo
	$(RUN_CMD) --profile extract --pipeline extract --input "$(DATA_DIR)" --output "$(BUILD_DIR)"
	@echo "OK: artifacts in $(BUILD_DIR)"

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

.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "};{printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
