FROM phusion/baseimage:latest
MAINTAINER m.snaith@dundee.ac.uk

# Get the necessary binaries
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.6 unzip lighttpd python-flup python-webpy python3-pip python-dev nginx

ADD ./src /app
ADD ./lib /lib
ADD requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt
RUN pip3 install uwsgi

ADD run.sh /
RUN chmod 777 /run.sh

ADD html /www/html

ADD dgep.conf /etc/nginx/sites-available/dgep
RUN ln -s /etc/nginx/sites-available/dgep /etc/nginx/sites-enabled

EXPOSE 8888

WORKDIR /app

#CMD ["python3", "/app/main.py"]

CMD ["/run.sh"]
