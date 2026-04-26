CC := cc
CFLAGS := -Wall -Wextra -std=c11
TARGET := app
OBJS := main.o math_utils.o

.PHONY: all help build run verify clean
all: help

help:
	@echo "Available targets:"
	@echo "  make build   # compile with dependencies"
	@echo "  make run     # build then run"
	@echo "  make verify  # run and check expected output"
	@echo "  make clean   # remove artifacts"

build: $(TARGET)

run: build
	./$(TARGET)

verify: build
	./$(TARGET) | grep -q "2 + 3 = 5"
	@echo "verify passed"

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(TARGET)

main.o: main.c math_utils.h
	$(CC) $(CFLAGS) -c main.c -o main.o

math_utils.o: math_utils.c math_utils.h
	$(CC) $(CFLAGS) -c math_utils.c -o math_utils.o

clean:
	rm -f $(TARGET) $(OBJS)
