SHELL = /bin/bash
GOALS = venv test dist clean tidy linux-executable windows-executable
.PHONY: help test dist clean tidy linux-executable windows-executable

help:
        @echo "choose a target from $(GOALS)."

venv: requirements.txt
        ( \
                virtualenv -p /usr/bin/python3 venv; \
                source venv/bin/activate; \
                pip install -U -r requirements.txt; true; \
        )

test: venv
        ( \
                source venv/bin/activate; \
                tests/test_panache.py; \
        )

dist: linux-executable windows-executable

linux-executable: dist/linux/panache

windows-executable: dist/windows/panache.exe

dist/linux/panache: src/panache.py
        docker run -e http_proxy="$(shell echo $$http_proxy)" -e https_proxy="$(shell echo $$http_proxy)" -v "$(shell pwd):/src/" cdrx/pyinstaller-linux

dist/windows/panache.exe: src/panache.py
        docker run -e http_proxy="$(shell echo $$http_proxy)" -e https_proxy="$(shell echo $$https_proxy)" -v "$(shell pwd):/src/" cdrx/pyinstaller-windows

clean:

tidy: clean
        rm -Rf dist
