# =========================
# Project variables
# =========================
SHELL        := /usr/bin/env bash
ACTIVATE       := . $(VENV_DIR)/bin/activate
SHELL        	:= /usr/bin/env bash

ROOT         	:= $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
TARGET  		:= $(ROOT)target
VENV         	:= $(ROOT).venv



DATA_DIR   		?= ./data
TMP_DIR    		?= ./tmp

PACK_CMD   := $(PY) -m spreadsheet_handling.cli pack
UNPACK_CMD := $(PY) -m spreadsheet_handling.cli unpack

SHA=$(shell git rev-parse --short HEAD)


PACK_CMD=$(PY) -m spreadsheet_handling.cli pack
UNPACK_CMD=$(PY) -m spreadsheet_handling.cli unpack

PACK_SETS=$(shell find $(DATA_DIR) -maxdepth 1 -mindepth 1 -type d -printf "%f\n")

.PHONY: pack unpack roundtrip verify extract clean

pack:
	@mkdir -p $(TMP_DIR)
	@for d in $(PACK_SETS); do \
		echo "Packing $$d -> $(TMP_DIR)/$$d-$(SHA).xlsx"; \
		$(PACK_CMD) --input $(DATA_DIR)/$$d --output $(TMP_DIR)/$$d-$(SHA).xlsx; \
	done


roundtrip: pack unpack  ## einfache Roundtrip-Demo (idempotenznah)

verify:
	@$(PY) scripts/verify.py  # wirft Fehler bei Verstoß -> bricht CI

extract:
	@mkdir -p $(TARGET)
	@$(PY) scripts/extract.py --data $(DATA_DIR) --out $(TARGET)

clean:
	rm -rf $(TMP_DIR) $(TARGET)

snapshot:
	@mkdir -p $(TARGET)
	@if [ -x "$(ROOT)tools/repo_snapshot.sh" ]; then \
	  "$(ROOT)tools/repo_snapshot.sh" "$(ROOT)" "$(TARGET)" "$(TARGET)/repo.txt"; \
	else \
	  echo "⚠️  script not found: $(ROOT)tools/repo_snapshot.sh"; \
	  echo "⚠️  not committed to this repo since non essential for the demo and would distract"; \
	  echo "⚠️  manually copy if needed: https://github.com/StefanSchade/spreadsheet-handling/tree/main/tools "; \
	fi