# Changelog
All notable changes to `explabox` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1]
### Fixed
- Several dependency bug fixes for March 2025

## [1.0.0]
### Added
- Example usage in Google Colab (requires `genbase>=0.2.17`)
- `explabox.explore.instances` to summarize instances in a split
- Selecting, sampling and filtering of `digestibles.Dataset`
- Support for Python 3.12

### Fixed
- Support for new pandas versions
- Bugfix where tokens are not properly filtered in `TokenFrequency` (requires `text-explainability>=0.6.6`)

## [0.9b7]
### Added
- Makefile for Windows (`make.bat`)
- License to each file
- Coverage testing on `codecov.io`
- Hosting documentation on `readthedocs.io`
- Dependencies for `explabox[dev]`, `explabox[docs]` and `explabox[all]`
- Contribution guide
- Software testing on Python `3.8`, `3.9` and `3.10`; for `windows`, `ubuntu` and `macos`
- Issue templates
- Pull request template
- Example usage with `explabox-demo-drugreview`
- Finished all docstrings
- Return `html` and `raw_html` from MultipleReturn
- Probability scores to feature contributions

### Changed
- Ported repository to GitHub
- CI/CD pipeline for GitHub actions

### Fixed
- Ensured stable dependency versions of `instancelib` and `text_explainability`
- `numpy.str` deprecation warning

### Removed
- Components from Gitlab repository

## [0.9b6]
### Added
- README.md
- Sphinx documentation
- Makefile
- License
- Requirements
- Dataset descriptives
- Installation guide
- Text sensitivity tests (`text_sensitivity`)
- Text explainability (`text_explainability`)
- Model importing (`genbase`)
- Dataset handling (`genbase`)
- Basic UI (`genbase`)
- `git` setup

[Unreleased]: https://github.com/MarcelRobeer/explabox
[1.0.1]: https://pypi.org/project/explabox/1.0.1
[1.0.0]: https://pypi.org/project/explabox/1.0.0
[0.9b6]: https://pypi.org/project/explabox/0.9b6
[0.9b7]: https://pypi.org/project/explabox/0.9b7
