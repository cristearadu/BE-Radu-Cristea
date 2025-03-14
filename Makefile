#!/bin/bash
.PHONY: setup test clean

setup:
	@echo "Checking Python version..."
	@if ! python3 --version | grep -q "3.10.8"; then \
		echo "Error: Python 3.10.8 is required. Please install the correct version."; \
		exit 1; \
	fi
	@echo "Python version is correct."

	@echo "Creating virtual environment..."
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
		echo "Virtual environment created."; \
	else \
		echo "Virtual environment already exists."; \
	fi

	@echo "Activating virtual environment and installing dependencies..."
	@.venv/bin/activate && pip install -r requirements.txt
	@echo "Setup complete."
