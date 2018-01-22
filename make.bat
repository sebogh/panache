@ECHO OFF

SETLOCAL

SET PDFLATEX_CMD=pdflatex


IF "%1"=="test" (
	CALL :TEST
) ELSE IF "%1"=="dist" (
	CALL :TEST
	CALL :DIST
) ELSE IF "%1"=="clean" (
	CALL :CLEAN
) ELSE IF "%1"=="tidy" (
	CALL :CLEAN
	CALL :TIDY
) ELSE IF "%1"=="installer" (
	CALL :INSTALLER
) ELSE IF "%1"=="help" (
	CALL :HELP
) ELSE (
	CALL :HELP
)

ENDLOCAL

GOTO :eof


:HELP
echo choose a target from "test", "clean", "tidy", "help", "installer"
GOTO :eof

:TEST
venv\Scripts\python.exe tests\test_panache.py
GOTO :eof

:DIST
echo make binaries at linux machine with docker
GOTO :eof

:INSTALLER
CALL make-windows-installer.bat
GOTO :eof

:CLEAN
del /Q /F panache.spec
del /Q /F *.wixobj
del /Q /F *.wixpdb
rmdir /Q /S build
rmdir /Q /S __pycache__
GOTO :eof

:TIDY
del /Q /F bin\panache.exe
del /Q /F bin\panache
del /Q /F bin\panache*.msi

GOTO :eof








