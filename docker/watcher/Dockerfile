FROM python:3

RUN pip3 install pipenv

# Switch to directory /usr/src/app inside the container
WORKDIR /usr/src/app

# Copy all files and folders from the local context directory into conatiner's working directory
COPY . .

RUN pipenv install

ENV PYTHONPATH "${PYTHONPATH}:."

CMD ["pipenv", "run", "python3", "./jmc/frugal/watcher/__main__.py"]
