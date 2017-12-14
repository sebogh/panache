SHELL = /bin/bash
GOALS = help venv test dist clean tidy
.PHONY: help test dist clean tidy

help:
	@echo "choose a target from $(GOALS)."

venv:
    virtualenv -p /usr/bin/python3 venv
    source venv/bin/activate
    pip install pyyaml

test: venv
    venv/bin/python tests/test_panache.py

dist: dist/panache

dist/panache: venv src/panache.py
    venv/bin/pyinstaller -p . --onefile src/panache.py --distpath=dist
    chmod 755 dist/panache

clean:
	rm -Rf panache.spec build __pycache__

tidy: clean
	rm -Rf dist

