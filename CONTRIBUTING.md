# Contributing
We would love for you to contribute and improve the `explabox`!

If you are unable to contribute yourself, feel free to post a [feature request or bug report](https://github.com/MarcelRobeer/explabox/issues/new/choose) for the developers and maintainers at the Netherlands *National Police Lab AI* (NPAI).

### 1. Getting started
- Make sure you have a GitHub account
- Submit a [ticket](https://github.com/MarcelRobeer/explabox/issues/new/choose) for your issue, assuming one does not already exist
- Fork the repository on GitHub

### 2. Setting up your environment
To ensure you are able to interactively edit and test your code, when contributing we recommend you install your forked version of the `explabox` with the `-e` (_editable_; i.e. `pip3 install -e .`) flag. Depending on where you want to contribute to, we have also provided you with the necessary optional packages required for quality checks and/or package building. These are:

- General development: `pip3 install -e ".[dev]"`
- Only working on documentation: `pip3 install -e ".[docs]"`

### 3. How to contribute
1. Choose a topic branch (typically `master`) to start your contribution from
2. Make commits of logical units
3. Ensure that if you contributed code you also include accompanying tests in the `explabox/test` folder
4. Perform all [quality checks](#quality-checks) when you are finished
5. Update the [changelog](#changelog) to state which contributions you made
6. Push your changes to a topic branch and create a [merge request](#merge-request), describing your contribution

<a name="quality-checks"/></a>
#### 3.1 Quality checks
When contributing to the `explabox`, you are required to adhere to several quality criteria, as described in the table below.
These are checked automatically when making a commit to the `main` branch (using `pre-commit`), and are included in the
`Makefile` (run `make quality` and `make coverage` in your terminal). In addition, they can be run manually with the
command provided in the _Manual check_ column below.

| Quality | Tool     | Description | Manual check |
|---------|----------|-------------|--------------|
| Import order | [`isort`](https://pycqa.github.io/isort/) | Imports in `.py` files are done in alphabetical order. | `isort --profile=black --line-length=120 --check-only .` |
| Linter  | [`black`](https://black.readthedocs.io/) | Automatic formatting of your `.py` code, weakened to a line length of 120. | `black --line-length=120 --check .` |
| Linter  | [`flake8`](https://flake8.pycqa.org/) | Minimal code style quality check, also weakened to a line length of 120. | `flake8 --config .flake8 .` |
| Security | [`bandit`](https://bandit.readthedocs.io/) | Software is checked for known security vulnerabilities. | `bandit -r explabox/ --configfile=.bandit.yaml` |
| Unit and integration testing | [`pytest`](https://docs.pytest.org/) | Software should be tested in seperate units and in combined pipelines. | `coverage run -m pytest` |
| `MANIFEST.in` completeness | [`check-manifest`](https://pypi.org/project/check-manifest/) | Check if all required files are also shipped with the Python package. | `check-manifest` |
| Documentation linter | [`doc8`](https://github.com/PyCQA/doc8) | Style checks for the documentation files that are used to generate [explabox.rtfd.io](https://explabox.rtfd.io) | `doc8 ./docs` |

These tools are automatically included when installing the `explabox` with the `[dev]` and `[all]` options. The documentation linter is installed with the `[doc]`, `[dev]` and `[all]` options.

<a name="changelog"/></a>
#### 3.2 Updating `CHANGELOG.md`
Update the changelog using the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) standard, under the `[Unreleased]` section of `CHANGELOG.md`. Contributions should be grouped under `### Added`, `### Changed`, `### Fixed` or `### Removed`. Note that you should not repeat the verb (e.g. _added_) of the group in a bullet point.

<a name="merge-request"/></a>
#### 3.3 Merge request
Clearly state your contributions when making a merge request. Reference any prior issues you are aiming to solve. If you require _new dependencies or new versions thereof_, also explicitly state why these are required.

Your contribution will be reviewed, potentially requiring changes to the code/documentation you have contributed. When passing all quality checks and the code review, your contribution will become part of the next version of the `explabox`.

#### 3.4 New version release
After a succesful merge request, the developers/maintainers of the `explabox` will ensure your contribution is pushed with the next version of the `explabox`.
