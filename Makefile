.PHONY: quality style

check_dirs := explabox

# Check style quality
quality:
	black --check $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 --config .flake8 $(check_dirs)

# Fix styles
style:
	black $(check_dirs)
	isort $(check_dirs)
