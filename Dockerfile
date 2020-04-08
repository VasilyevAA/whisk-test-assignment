FROM selenium/base:latest

ENV ALLURE_DIR="./allure-results/" \
    TESTS_DIR="./tests" \
    TEST_THREAD_COUNT="5" \
    TEST_TIMEOUT="200" \
    PYTEST_STOUT="-vvv -s"

USER root

RUN apt update \
    && apt install -y python3.7 python3-pip

RUN mkdir -p /app
WORKDIR /app

COPY /requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -U pip \
    && pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["run.sh"]
CMD [""]