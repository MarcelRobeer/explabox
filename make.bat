@echo off


IF /I "%1"=="package " GOTO package
IF /I "%1"=="check_dirs " GOTO check_dirs
IF /I "%1"=="docs_dir " GOTO docs_dir
IF /I "%1"=="build_dir " GOTO build_dir
IF /I "%1"=="source_dir " GOTO source_dir
IF /I "%1"=="docs" GOTO docs
IF /I "%1"=="html" GOTO html
IF /I "%1"=="quality" GOTO quality
IF /I "%1"=="precommit" GOTO precommit
IF /I "%1"=="coverage" GOTO coverage
GOTO error

:package
	CALL make.bat =
	CALL make.bat explabox
	GOTO :EOF

:check_dirs
	CALL make.bat =
	CALL make.bat $(package)
	GOTO :EOF

:docs_dir
	CALL make.bat =
	CALL make.bat docs
	GOTO :EOF

:build_dir
	CALL make.bat =
	CALL make.bat $(docs_dir)/build
	GOTO :EOF

:source_dir
	CALL make.bat =
	CALL make.bat $(docs_dir)/source
	GOTO :EOF

:docs
	XCOPY /Y img/%package%-logo-text.png %source_dir%/_static
	sphinx-apidoc --module-first --no-toc --force --templatedir=%source_dir%/_templates/ -o %source_dir%/api explabox
	XCOPY /Y CHANGELOG.md %source_dir%/changelog.md
	XCOPY /Y CONTRIBUTING.md %source_dir%/contributing.md
	XCOPY /Y INSTALLATION.md %source_dir%/installation.md
	XCOPY /Y EXAMPLE_USAGE.md %source_dir%/example-usage.md
	GOTO :EOF

:html
	sphinx-build -M clean %source_dir% %build_dir%
	sphinx-build -M html %source_dir% %build_dir%
	GOTO :EOF

:quality
	python3 -m black --line-length=120 --check explabox
	python3 -m isort --line-length=120 --profile=black --check-only explabox
	python3 -m flake8 explabox --config .flake8
	python3 -m doc8 ./docs
	check-manifest
	GOTO :EOF

:precommit
	pre-commit run
	GOTO :EOF

:coverage
	python3 -m coverage run -m pytest
	python3 -m coverage html
	open htmlcov/index.html
	GOTO :EOF

:error
    IF "%1"=="" (
        ECHO make: *** No targets specified and no makefile found.  Stop.
    ) ELSE (
        ECHO make: *** No rule to make target '%1%'. Stop.
    )
    GOTO :EOF
