SHELL = /bin/bash
GOALS = venv test dist clean tidy
.PHONY: help test dist clean tidy

help:
	@echo "choose a target from $(GOALS)."

venv:
	( \
		virtualenv -p /usr/bin/python3 venv; \
		source venv/bin/activate; \
		pip install -r requirements.txt; 
	)

test: venv
	( \
		source venv/bin/activate; \
		tests/test_panache.py; \
	)


dist: dist/panache

dist/panache: venv src/panache.py
	( \
		source venv/bin/activate; \
		pyinstaller -p . --onefile src/panache.py --distpath=dist; \
		chmod 755 dist/panache; \
	\)

clean:
	rm -Rf panache.spec build __pycache__

tidy: clean
	rm -Rf dist

