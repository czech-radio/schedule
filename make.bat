@ECHO OFF

pushd %~dp0

REM Command file for this project.

set SOURCE=source

if "%1" == "" goto help

if "%1" == "test" (
	pytest
	exit /b 1
)

if "%1" == "lint" (
	black .
	isort . --profile black
	exit /b 1
)

if "%1" == "check" (
    black . --check  --exclude "(docs/|build/|dist/|\.git/|\.mypy_cache/|\.tox/|\.venv/\.asv/|env|\.eggs)"
    isort . --check --profile black
	flake8 src/cro --count --select=E9,F63,F7,F82 --show-source --statistics
	pytest
	exit /b 1
)

REM Quick README update commit.
if "%1" == "quick" (
    git commit -am "Update README"
)

goto end

:help
echo There will be hellp message.

:end
popd
