FROM python:3

RUN pip3 install pipenv

RUN useradd -m -s /bin/bash jenkins

WORKDIR /usr/src/app

USER jenkins

# Copy all files and folders from the local context directory into conatiner's working directory
COPY . .

RUN pipenv install --dev

ENV PYTHONPATH "${PYTHONPATH}:."
