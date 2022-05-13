.PHONY: docs html quality precommit coverage

package := explabox
check_dirs := $(package)
docs_dir := docs
build_dir := $(docs_dir)/build
source_dir := $(docs_dir)/source

# Build documentation files
docs:
	cp img/$(package)-logo-text.png $(source_dir)/_static
	sphinx-apidoc --module-first --no-toc --force --templatedir=$(source_dir)/_templates/ -o $(source_dir)/api .
	m2r CHANGELOG.md --dry-run > $(source_dir)/changelog.rst
	m2r CONTRIBUTING.md --dry-run > $(source_dir)/contributing.rst
	m2r INSTALLATION.md --dry-run > $(source_dir)/installation.rst
	m2r EXAMPLE_USAGE.md --dry-run > $(source_dir)/example-usage.rst

# Convert docs to HTML
html:
	sphinx-build -M clean $(source_dir) $(build_dir)
	sphinx-build -M html $(source_dir) $(build_dir)

# Check style quality
quality:
	python3 -m black --line-length=120 --check .
	python3 -m isort --profile=black --check-only .
	python3 -m flake8 --config .flake8 .
	python3 -m doc8 ./docs
	python3 -m check-manifest

# Fix styles and check security issues
precommit:
	pre-commit run

# Coverage
coverage:
	coverage run -m pytest
	coverage html
	open htmlcov/index.html
