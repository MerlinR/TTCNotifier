CWD:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SRC_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))/TTCNotify

setup:
	@echo "Installing dependences"
	pip install -r requirements.txt

test:
	@echo "Running Unit Tests"
	@echo "Not implemented"

clean:
	find . -name "*.pyc" -type f -delete
