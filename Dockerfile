FROM arg-tech/ws:python-0.1

MAINTAINER m.snaith@dundee.ac.uk

ADD ./src /app
ADD ./lib /lib
ADD requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

WORKDIR /app

ENV APP_NAME dgep
ENV VERSION 1.0.1
ENV HOST localhost:8888
