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
	isort .
	exit /b 1
)

if "%1" == "check" (
    black .
    isort .
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
