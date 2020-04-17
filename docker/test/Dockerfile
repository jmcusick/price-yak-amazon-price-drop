FROM python:3

RUN pip3 install pipenv

RUN useradd -m -s /bin/bash jenkins

# Switch user and to home directory
USER jenkins
WORKDIR /home/jenkins # wont be created as root, since created w/ useradd -m

# Copy all files and folders from the local context directory into conatiner's working directory
COPY . .

RUN pipenv install

ENV PYTHONPATH "${PYTHONPATH}:."
