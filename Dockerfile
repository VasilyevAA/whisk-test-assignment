FROM selenium/base:latest

ENV ALLURE_DIR="./allure-results/" \
    TESTS_DIR="./tests" \
    TEST_THREAD_COUNT="5" \
    TEST_TIMEOUT="120" \
    PYTEST_STOUT="-vvv -s"

USER root

RUN apt update \
    && apt install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt install -y python3.8 python3-pip \
    && unlink /usr/bin/python3 \
    && ln -s /usr/bin/python3.8 /usr/bin/python3


RUN mkdir -p /app
WORKDIR /app

COPY /requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -U pip \
    && pip3 install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["/app/run.sh"]
CMD [""]