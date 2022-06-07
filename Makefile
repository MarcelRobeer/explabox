.PHONY: docs html quality precommit coverage

package := explabox
check_dirs := $(package)
docs_dir := docs
build_dir := $(docs_dir)/build
source_dir := $(docs_dir)/source

# Build documentation files
docs:
	cp img/$(package)-logo-text.png $(source_dir)/_static
	sphinx-apidoc --module-first --no-toc --force --templatedir=$(source_dir)/_templates/ -o $(source_dir)/api explabox
	cp CHANGELOG.md $(source_dir)/changelog.md
	cp CONTRIBUTING.md $(source_dir)/contributing.md
	cp INSTALLATION.md $(source_dir)/installation.md
	cp EXAMPLE_USAGE.md $(source_dir)/example-usage.md

# Convert docs to HTML
html:
	sphinx-build -M clean $(source_dir) $(build_dir)
	sphinx-build -M html $(source_dir) $(build_dir)

# Check style quality
quality:
	python3 -m black --line-length=120 --check explabox
	python3 -m isort --line-length=120 --profile=black --check-only explabox
	flake8 explabox --config .flake8
	python3 -m doc8 ./docs
	check-manifest

# Fix styles and check security issues
precommit:
	pre-commit run

# Coverage
coverage:
	coverage run -m pytest
	coverage html
	open htmlcov/index.html
