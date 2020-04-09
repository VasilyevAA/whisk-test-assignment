
build:
	docker-compose build --pull

testing_all:
	docker-compose run --rm testing

testing_ui:
	docker-compose run --rm -e TESTS_DIR='./tests/ui' testing

testing_api:
	docker-compose run --rm -e TESTS_DIR='./tests/api' testing
