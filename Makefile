precommit: docs style quality

.PHONY: docs quality style

package := explabox
check_dirs := $(package)

# Build documentation files
docs:
	sphinx-apidoc --module-first --no-toc --force -o docs/source/api $(package)

# Check style quality
quality:
	black --check $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 --config .flake8 $(check_dirs)

# Fix styles
style:
	black $(check_dirs)
	isort $(check_dirs)
