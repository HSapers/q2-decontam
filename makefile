.PHONY: all lint dev run

all: ;

run: all
	qiime decontam hello --o-text example_greeting --verbose
	qiime decontam text-vis --i-greeting example_greeting.qza --o-visualization example_greeting

lint: all
	flake8

dev: all
	pip install -e .
	qiime dev refresh-cache

test: all
	py.test

test-cov: all
	py.test --cov=q2_decontam --cov-report=term-missing

clean: all
	rm example_greeting.qz*
