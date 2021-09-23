.PHONY: all lint dev run

all: ;

run:
	qiime decontam hello --o-text example_greeting --verbose

lint:
	flake8

dev: all
	pip install -e .