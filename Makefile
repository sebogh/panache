SHELL = /bin/bash

MY_UID = $(shell id -u)
MY_GID = $(shell id -g)

VERSION = $(shell cat panache/version.py | grep -P '(?<=^version = ")\d+\.\d+\.\d+' -o)

FIX_OWNERSHIP = docker run -v "$(shell pwd):/thedir" -it debian:stable-slim /bin/bash -c "chown -R ${MY_UID}:${MY_GID} /thedir"

GOALS = venv test dist clean tidy linux-executable windows-executable
.PHONY: help test dist clean tidy linux-executable windows-executable msi-installer fix-ownership

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

dist: linux-executable windows-executable msi-installer

linux-executable: ./bin/panache

windows-executable: ./bin/panache.exe

msi-installer: ./bin/panache-${VERSION}.msi

fix-ownership: 
	docker run -v "$(shell pwd):/panache" -it debian:stable-slim /bin/bash -c "chown -R ${MY_UID}:${MY_GID} /panache"

./bin/panache: panache/panache.py test
	( \
		source venv/bin/activate; \
		pyinstaller --onefile panache/panache.py --distpath=bin; \
		chmod 755 bin/panache; \
	)

./bin/panache.exe: panache/panache.py test
	docker run -e http_proxy="$(shell echo $$http_proxy)" -e https_proxy="$(shell echo $$https_proxy)" -v "$(shell pwd):/panache/" cdrx/pyinstaller-windows \
	; ret=$$? \
	; $(FIX_OWNERSHIP) \
	; exit $$ret
	mkdir -p bin
	mv ./dist/windows/panache.exe ./bin

./bin/panache-$(VERSION).msi: ./bin/panache.exe
	docker run -v "$(shell pwd):/panache" -it debian:stable-slim /bin/bash -c "chown -R 1000:1000 /panache"
	docker run -v "$(shell pwd):/panache" -it justmoon/wix /bin/bash -c "cd /panache && /usr/bin/wine /home/wix/wix/candle.exe -dVERSION=${VERSION} panache.wxs && /usr/bin/wine /home/wix/wix/light.exe -sval panache.wixobj -out bin/panache-${VERSION}.msi" \
	; ret=$$? \
	; $(FIX_OWNERSHIP) \
	; chmod 755 ./bin/panache-$(VERSION).msi \
	; exit $$ret

clean:
	rm -Rf dist build venv
	rm -f panache.wixobj bin/panache-${VERSION}.wixpdb *~

tidy: clean
	rm -Rf ./bin
