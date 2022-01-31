.PHONY: help

SHELL        = /bin/bash
# export PATH := bin:$(PATH)

setup-dev:
	rm -rf .venv && \
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	python3 -m pip install --upgrade pip && \
	pip install poetry && \
	poetry install

# Run the rabbit backend so that we can do better debugging of the webhook
run-rabbit:
	lima nerdctl run -d --name rabbitmq-management -p 5672:5672 -p 8080:15672 rabbitmq:3.8.9-management

run-webhook: run-rabbit
	(source .venv/bin/activate && \
	set -a && \
	source .env && \
	cd src && \
	python3 -m cava.webhook.main &)

run-correlator: run-webhook
	source .venv/bin/activate && \
	set -a && \
	source .env && \
	cd src && \
	python3 -m cava.correlator.main

killall: stop-rabbit
	killall python3

stop-rabbit:
	lima nerdctl rm -f rabbitmq-management

help:
	@echo "Usage: make {run-rabbit|run-webhook|stop-rabbit|run-correlator|help}" 1>&2 && false
