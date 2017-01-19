
PIP := pip3
PYTHON := python3
PYTHON_UNDEV := python3
TWINE := twine

-include local.mk

.PHONY: default dev publish clean init test undev

default: test

init:
	$(PIP) install -r requirements.txt --upgrade

dev:
	$(PIP) install -e .

undev:
	$(PYTHON_UNDEV) setup.py develop --uninstall

test:
	$(PYTHON) setup.py test

publish: clean
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	$(TWINE) upload dist/*

clean:
	rm -rf dist pylaser.egg-info build
