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
ELSE IF "%1"=="help" (
	CALL :HELP
) ELSE (
	CALL :HELP
)

ENDLOCAL

GOTO :eof


:HELP
echo choose a target from "test", "dist", "clean", "tidy", "help"
GOTO :eof

:TEST
venv\Scripts\python.exe tests\test_panache.py
GOTO :eof

:DIST
venv\Scripts\pyinstaller -p . --onefile src\panache.py --distpath=bin
GOTO :eof

:CLEAN
del /Q /F panache.spec
rmdir /Q /S build
rmdir /Q /S __pycache__
GOTO :eof

:TIDY
rmdir /Q /S bin/panache.exe
GOTO :eof








