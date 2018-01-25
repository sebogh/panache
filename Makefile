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

linux-executable: src/panache.py
	docker run -e http_proxy="$(shell echo $$http_proxy)" -e https_proxy="$(shell echo $$http_proxy)" -v "$(shell pwd):/src/" cdrx/pyinstaller-linux

windows-executable: src/panache.py
	docker run -e http_proxy="$(shell echo $$http_proxy)" -e https_proxy="$(shell echo $$https_proxy)" -v "$(shell pwd):/src/" cdrx/pyinstaller-windows

clean:

tidy: clean
	rm -Rf dist


