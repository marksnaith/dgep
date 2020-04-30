FROM phusion/baseimage:latest
MAINTAINER m.snaith@dundee.ac.uk

# Get the necessary binaries
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.6 unzip lighttpd python-flup python-webpy python3-pip python-dev

ADD ./src /app
ADD ./lib /lib
ADD requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

EXPOSE 8888

CMD ["python3", "/app/main.py"]
