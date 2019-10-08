ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
APP_DIR:="${ROOT_DIR}/app"
TESTS_DIR:="${ROOT_DIR}/tests"
CODE_QUALITY_DIR:="${ROOT_DIR}/code_quality"
SHELL := /bin/bash
COMPUTED_ENV="${ROOT_DIR}/set_env.py"
.PHONY: all code-quality tests set-env postgres-permission setup up rebuild-req

all: up

code-quality:
	cd "${CODE_QUALITY_DIR}" && make

tests:
	cd "${TESTS_DIR}" && make

show-env:
	env | grep -i latigo

postgres-permission:
	sudo mkdir "${ROOT_DIR}/volumes/postgres" -p && sudo chown -R lroll:lroll "${ROOT_DIR}/volumes/postgres"

# Rebuild latest latigo and install it to site-packages before starting tests
setup:
	rm -rf app/build
	pip uninstall -y latigo
	pip install app/

build: postgres-permission setup code-quality tests show-env
	docker-compose build

up: build
	docker-compose up


rebuild-req:
	pip uninstall gordo-components -y
	pip install --upgrade pip-tools
	cd app && cat requirements.in | sort -u > r.in
	cd app && pip-compile --output-file=requirements.txt r.in
	cd app && cat requirements.in, test_requirements.in | sort -u > r.in
	cd app && pip-compile --output-file=test_requirements.txt r.in
