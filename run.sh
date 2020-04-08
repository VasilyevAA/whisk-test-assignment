#!/bin/sh -e

RUNMODE="${1:-pytest}"

if [ "${RUNMODE}" = "pytest" ]; then
  PYTEST_DEFAULT="pytest --execution-timeout ${TEST_TIMEOUT} ${PYTEST_STOUT} --alluredir=${ALLURE_DIR} -n ${TEST_THREAD_COUNT} ${TESTS_DIR}"
  echo "${PYTEST_DEFAULT}"
  ${PYTEST_DEFAULT}
else
  ${RUNMODE}
fi