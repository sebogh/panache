#!/bin/bash

#virtualenv -p /usr/bin/python3 venv
#source venv/bin/activate
#pip install pandocfilters
#pip install pyinstaller


venv/bin/pyinstaller -p . --onefile pandoctc.py --distpath=dist
chmod 755 dist/pandoctc
