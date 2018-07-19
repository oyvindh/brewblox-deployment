FROM python:3.6

ENV TEST_HOST=127.0.0.1

COPY . /app
WORKDIR /app

RUN pip3 install pipenv
RUN pipenv install --dev

ENTRYPOINT [ "pipenv", "run", "pytest" ]
