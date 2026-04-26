OUT_DIR := out

.PHONY: all pipeline prepare train eval report verify clean help
all: help

help:
	@echo "Available targets:"
	@echo "  make prepare   # generate prepared dataset artifact"
	@echo "  make train     # generate model artifact"
	@echo "  make eval      # generate metrics artifact"
	@echo "  make report    # generate report artifact"
	@echo "  make pipeline  # run prepare -> train -> eval -> report"
	@echo "  make verify    # assert required artifacts exist"
	@echo "  make clean     # remove generated artifacts"

pipeline: report

prepare: $(OUT_DIR)/prepared.txt
train: $(OUT_DIR)/model.txt
eval: $(OUT_DIR)/metrics.txt
report: $(OUT_DIR)/report.txt

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

$(OUT_DIR)/prepared.txt: | $(OUT_DIR)
	echo "dataset=demo" > $(OUT_DIR)/prepared.txt
	echo "status=prepared" >> $(OUT_DIR)/prepared.txt

$(OUT_DIR)/model.txt: $(OUT_DIR)/prepared.txt
	echo "model=tiny-baseline" > $(OUT_DIR)/model.txt
	echo "trained_on=$$(date '+%Y-%m-%d %H:%M:%S')" >> $(OUT_DIR)/model.txt

$(OUT_DIR)/metrics.txt: $(OUT_DIR)/model.txt
	echo "accuracy=0.92" > $(OUT_DIR)/metrics.txt
	echo "latency_ms=35" >> $(OUT_DIR)/metrics.txt

$(OUT_DIR)/report.txt: $(OUT_DIR)/metrics.txt
	echo "# Demo Report" > $(OUT_DIR)/report.txt
	cat $(OUT_DIR)/prepared.txt >> $(OUT_DIR)/report.txt
	cat $(OUT_DIR)/model.txt >> $(OUT_DIR)/report.txt
	cat $(OUT_DIR)/metrics.txt >> $(OUT_DIR)/report.txt
	@echo "Report generated at $(OUT_DIR)/report.txt"

verify: pipeline
	test -f $(OUT_DIR)/prepared.txt
	test -f $(OUT_DIR)/model.txt
	test -f $(OUT_DIR)/metrics.txt
	test -f $(OUT_DIR)/report.txt
	grep -q "accuracy=0.92" $(OUT_DIR)/metrics.txt
	@echo "verify passed"

clean:
	rm -rf $(OUT_DIR)
