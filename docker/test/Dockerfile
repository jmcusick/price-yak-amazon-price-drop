FROM python:3

RUN pip3 install pipenv

ARG JENKINS_UID
RUN test -n "$JENKINS_UID"

ARG JENKINS_GID
RUN test -n "$JENKINS_GID"

RUN groupadd -g "$JENKINS_GID" jenkins

RUN useradd -m -s /bin/bash -u "$JENKINS_UID" -g "$JENKINS_GID" jenkins

# RUN useradd -m -s /bin/bash jenkins

# won't be created by root, since already exists
WORKDIR /home/jenkins

ENV DOCKER_WORKDIR /home/jenkins

USER jenkins

# Copy all files and folders from the local context directory into conatiner's working directory
COPY --chown=jenkins:jenkins . .

RUN pipenv install --dev

ENV PYTHONPATH "${PYTHONPATH}:."
