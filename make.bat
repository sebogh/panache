@ECHO OFF

venv\Scripts\pyinstaller -p . --onefile panache\panache.py --distpath=dist

