CC := cc
CFLAGS := -Wall -Wextra -std=c11
TARGET := hello_make
SRC := demo_single_file.c

.PHONY: all help build run verify clean
all: help

help:
	@echo "Available targets:"
	@echo "  make build   # compile binary"
	@echo "  make run     # build then run"
	@echo "  make verify  # build and smoke check output"
	@echo "  make clean   # remove artifacts"

build: $(TARGET)

run: build
	./$(TARGET)

verify: build
	./$(TARGET) | grep -q "Hello from make demo"
	@echo "verify passed"

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)
