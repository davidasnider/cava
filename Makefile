.PHONY: help

SHELL        = /bin/bash
# export PATH := bin:$(PATH)

# Run the rabbit backend so that we can do better debugging of the webhook
run-rabbit:
	docker run -d --name rabbitmq-management --rm -p 5672:5672 -p 8080:15672 --env-file .env rabbitmq:3.8.9-management

run-webhook: run-rabbit
	(source .venv/bin/activate && \
	source .env && \
	cd src && \
	python3 -m cava.webhook.main  && \
	cd .. && \
	make stop-rabbit)

stop-rabbit:
	docker stop rabbitmq-management

help:
	@echo "Usage: make {run-rabbit|run-webhook|help}" 1>&2 && false
