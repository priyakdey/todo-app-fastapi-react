.PHONY: setup clean

setup:
	docker-compose -f stack.yml up -d

teardown:
	docker-compose -f stack.yml down -v

