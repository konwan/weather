FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /opt/weather
RUN apt-get update && apt-get install -y cron vim
RUN cd /opt/docker && wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && tar jxvf phantomjs-2.1.1-linux-x86_64.tar.bz2 && rm phantomjs-2.1.1-linux-x86_64.tar.bz2
ADD requirements.txt /opt/weather
RUN cd /opt/weather && pip install -r requirements.txt
WORKDIR /opt/weather
ADD . /opt/weather
