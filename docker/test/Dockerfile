FROM python:3

RUN pip3 install pipenv

# RUN groupadd -g 994 jenkins

# RUN useradd -m -s /bin/bash -u 996 -g 994 jenkins

RUN useradd -m -s /bin/bash jenkins

# won't be created by root, since already exists
WORKDIR /home/jenkins

# COPY assigns root ownership by default (regardless of USER)
COPY --chown=jenkins:jenkins . .

USER jenkins

RUN pipenv install --dev

ENV PYTHONPATH "${PYTHONPATH}:."
