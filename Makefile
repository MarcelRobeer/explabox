precommit: style quality docs

.PHONY: docs html quality style

package := explabox
check_dirs := $(package)
docs_dir := docs
build_dir := $(docs_dir)/build
source_dir := $(docs_dir)/source

# Build documentation files
docs:
	cp img/$(package)-logo-text.png $(source_dir)/_static
	sphinx-apidoc --module-first --no-toc --force -o $(source_dir)/api $(package)
	m2r CHANGELOG.md --dry-run > $(source_dir)/changelog.rst
	m2r CONTRIBUTING.md --dry-run > $(source_dir)/contributing.rst
	m2r INSTALLATION.md --dry-run > $(source_dir)/installation.rst

# Convert docs to HTML
html:
	sphinx-build -M clean $(source_dir) $(build_dir)
	sphinx-build -M html $(source_dir) $(build_dir)

# Check style quality
quality:
	black --line-length=120 --check $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 --config .flake8 $(check_dirs)

# Fix styles
style:
	black --line-length=120 $(check_dirs)
	isort $(check_dirs)
