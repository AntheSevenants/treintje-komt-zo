FROM python:3.9-slim

WORKDIR /usr/app/src

RUN apt-get update
RUN apt-get install -y cron

ADD .docker/crontab /crontab
RUN /usr/bin/crontab /crontab

# For testing, we map source code directly to /usr/app/src
# (in the volume mapping)

# Then, copy the requirements manually
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "bash", "./.docker/cron.sh" ]