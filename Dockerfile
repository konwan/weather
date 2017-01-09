FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /opt/weather
WORKDIR /opt/weather
RUN apt-get update && apt-get install -y cron vim && cat getdata.cron >> /var/spool/cron/crontabs/root
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && tar jxvf phantomjs-2.1.1-linux-x86_64.tar.bz2 && rm phantomjs-2.1.1-linux-x86_64.tar.bz2 && ln -s phantomjs-2.1.1-linux-x86_64 phantomjs
ADD requirements.txt /opt/weather
RUN pip install -r requirements.txt
ADD . /opt/weather
CMD /bin/bash

