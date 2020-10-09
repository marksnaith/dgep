FROM python:3.7-stretch
MAINTAINER mark@arg.tech

# Get the necessary binaries
<<<<<<< Updated upstream
RUN apt-get update && \
    apt-get install -y python3-pip python-dev git-all &&\
    apt-get clean
=======
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.6 unzip lighttpd python-flup python-webpy python3-pip python-dev nginx
>>>>>>> Stashed changes

# Update pip
RUN pip3 install --upgrade pip

<<<<<<< Updated upstream
# Add the DGEP library
ADD src /lib/dgep
=======
RUN pip3 install -r /app/requirements.txt
RUN pip3 install uwsgi

ADD run.sh /
RUN chmod 777 /run.sh

ADD html /www/html

ADD dgep.conf /etc/nginx/sites-available/dgep
RUN ln -s /etc/nginx/sites-available/dgep /etc/nginx/sites-enabled
>>>>>>> Stashed changes

# Install DGEP
WORKDIR /lib/dgep
RUN pip3 install .

<<<<<<< Updated upstream
RUN pip3 freeze
=======
WORKDIR /app

#CMD ["python3", "/app/main.py"]

CMD ["/run.sh"]
>>>>>>> Stashed changes
