# Whisk test assignment

## Tasks

1) UI/E2E:
несколько простых тестов (можно для разных браузеров) - типа зарегить пользователя, добавить что-то в лист, удалить
в идеале в контейнере (https://dev.whisk.com/)

2) API:
Создать шопинг-лист, добавить в шопинг лист 1 итем, проверить, что он добавлен и удалить его.
Понятно что еще понадобится авторизоваться. Если ещё будет логин/логаут - будет хорошо.
(https://developers.whisk.com)

## Environment:
0) Use Unix like OS
1) Install docker
2) Install docker-compose
3) Install make

## How to use
1) Set credentials in docker-compose.override.yaml (required: WHISK_CLIENT_ID, BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY)
2) make build
3) And choose one of command with make: testing_all, testing_api, testing_ui 

For configure remote browsers for UI tests change "browser_config.json" items. 
Remote config you can find [here](https://www.browserstack.com/automate/python) 
in "Getting Started" copy "desired_cap" from snippet
