FROM python:3.7-stretch
MAINTAINER mark@arg.tech

# Get the necessary binaries
RUN apt-get update && \
    apt-get install -y python3-pip python-dev git-all &&\
    apt-get clean

# Update pip
RUN pip3 install --upgrade pip

# Add the DGEP library
ADD src /lib/dgep

# Install DGEP
WORKDIR /lib/dgep
RUN pip3 install .

RUN pip3 freeze
