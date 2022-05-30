
Contributing
============

...


1. Getting started
^^^^^^^^^^^^^^^^^^


* Make sure you have a GitHub account
* ...
* Fork the repository on GitHub

2. Setting up your environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To ensure you are able to interactively edit and test your code, when contributing we recommend you install your forked version of the ``explabox`` with the ``-e`` (\ *editable*\ ; i.e. ``pip3 install -e .``\ ) flag. Depending on where you want to contribute to, we have also provided you with the necessary optional packages required for quality checks and/or package building. These are:


* General development: ``pip3 install -e ".[dev]"``
* Only working on documentation: ``pip3 install -e ".[docs]"``

3. How to contribute
^^^^^^^^^^^^^^^^^^^^

...


3.1 Quality checks
~~~~~~~~~~~~~~~~~~

When contributing to the ``explabox``\ , you are required to adhere to several quality criteria, as described in the table below.
These are checked automatically when making a commit to the ``main`` branch (using ``pre-commit``\ ), and are included in the
``Makefile`` (run ``make quality`` and ``make coverage`` in your terminal). In addition, they can be run manually with the
command provided in the *Manual check* column below.

.. list-table::
   :header-rows: 1

   * - Quality
     - Tool
     - Description
     - Manual check
   * - Import order
     - `\ ``isort`` <https://pycqa.github.io/isort/>`_
     - Imports in ``.py`` files are done in alphabetical order.
     - ``isort --profile=black --line-length=120 --check-only .``
   * - Linter
     - `\ ``black`` <https://black.readthedocs.io/>`_
     - Automatic formatting of your ``.py`` code, weakened to a line length of 120.
     - ``black --line-length=120 --check .``
   * - Linter
     - `\ ``flake8`` <https://flake8.pycqa.org/>`_
     - Minimal code style quality check, also weakened to a line length of 120.
     - ``flake8 --config .flake8 .``
   * - Security
     - `\ ``bandit`` <https://bandit.readthedocs.io/>`_
     - Software is checked for known security vulnerabilities.
     - ``bandit -r explabox/ --configfile=.bandit.yaml``
   * - Unit testing
     - `\ ``pytest`` <https://docs.pytest.org/>`_
     - Software should be close to 100% ``coverage`` of .
     - ``coverage run -m pytest``
   * - MANIFEST.in completeness
     - `\ ``check-manifest`` <https://pypi.org/project/check-manifest/>`_
     - Check if all required files are also shipped with the Python package.
     - ``check-manifest``
   * - Documentation linter
     - `\ ``doc8`` <https://github.com/PyCQA/doc8>`_
     - Style checks for the documentation files that are used to generate `explabox.rtfd.io <https://explabox.rtfd.io>`_
     - ``doc8 ./docs``


These tools are automatically included when installing the ``explabox`` with the ``[dev]`` and ``[all]`` options. The documentation linter is installed with the ``[doc]``\ , ``[dev]`` and ``[all]`` options.

3.2 Updating ``CHANGELOG.md``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

...


3.3 Merge request
~~~~~~~~~~~~~~~~~

...


3.4 New version release
~~~~~~~~~~~~~~~~~~~~~~~

...

