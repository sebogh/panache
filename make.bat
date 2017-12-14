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
venv\Scripts\python tests\test_panache.py
GOTO :eof

:DIST
venv\Scripts\pyinstaller -p . --onefile panache\panache.py --distpath=dist
GOTO :eof

:CLEAN
del /Q /F panache.spec
del /Q /S build
GOTO :eof

:TIDY
del /Q /S dist
GOTO :eof








