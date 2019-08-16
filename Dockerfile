FROM python:3

RUN pip3 install pipenv

ADD . /usr/src/app
WORKDIR /usr/src/app
