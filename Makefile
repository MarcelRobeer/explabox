precommit: docs style quality

.PHONY: docs html quality style

package := explabox
check_dirs := $(package)
docs_dir := docs
build_dir := $(docs_dir)/build
source_dir := $(docs_dir)/source

# Build documentation files
docs:
	sphinx-apidoc --module-first --no-toc --force -o $(docs_dir)/$(source_dir)/api $(package)

# Convert docs to HTML
html:
	sphinx-build -M clean $(source_dir) $(build_dir)
	sphinx-build -M html $(source_dir) $(build_dir)

# Check style quality
quality:
	black --check $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 --config .flake8 $(check_dirs)

# Fix styles
style:
	black $(check_dirs)
	isort $(check_dirs)
