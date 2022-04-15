@ECHO OFF

pushd %~dp0

REM Command file for this project.

set SOURCE=source

if "%1" == "" goto help

if "%1" == "build" (
    black .
    isort .
	pytest
	exit /b 1
)
goto end

:help
echo There will be hellp message.

:end
popd
