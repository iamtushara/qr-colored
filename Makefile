export SHELL:=/bin/bash

.ONESHELL:

init: 
	mkdir -p build

clean:
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf .coverage.ip*
	rm -rf build/
	rm -rf ./tmp
	find . -type f -name "*.py[co]" -delete -or -type d -name "__pycache__" -delete

test: init
	python -m pytest --junitxml=build/test_report.xml tests/ --cov --cov-report=term | tee build/test.out

lint: init
	pylint --disable=all --enable -d,C qr_colored/*.py | tee build/lint.out

mypy: init
	mypy --ignore-missing-imports qr_colored/*.py | tee build/mypy.out
	rm -rf .mypy_cache

package_path: init
	conda build conda.recipe --output

release: init
	conda build conda.recipe

all: clean test lint release
