precommit: docs style quality

.PHONY: docs html quality style

package := explabox
check_dirs := $(package)
source_dir := source
build_dir := build

# Build documentation files
docs:
	sphinx-apidoc --module-first --no-toc --force -o docs/$(source_dir)/api $(package)

# Convert docs to HTML
html:
	sphinx-build -M clean docs/$(source_dir) docs/$(build_dir)
	sphinx-build -M html docs/$(source_dir) docs/$(build_dir)

# Check style quality
quality:
	black --check $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 --config .flake8 $(check_dirs)

# Fix styles
style:
	black $(check_dirs)
	isort $(check_dirs)
