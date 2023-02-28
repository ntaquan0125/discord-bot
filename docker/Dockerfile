FROM ubuntu:20.04 as main

WORKDIR /pif

# ADD repositories /etc/apk/repositories

#Install python 3
# RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update 
RUN apt-get install -y python3.9
RUN apt install -y python3-pip
RUN apt install -y build-essential libssl-dev libffi-dev python3-dev

#Install other platform requirement
RUN apt install -y ffmpeg libcairo2-dev libgirepository1.0-dev libdbus-glib-1-dev

# Install utility
RUN apt-get update && \
    apt-get install -y pkg-config &&\
    pip install -U setuptools wheel

RUN pip install opencv-python==4.7.0.68

FROM main as dev

# Install utility
RUN apt update && \
    pip install -U black

ADD ./requirements.txt /pif/bot-playground/

# Download and install pip package
RUN pip install --upgrade pip
RUN pip install -r /pif/bot-playground/requirements.txt

#Copy file
ADD ./ /pif/bot-playground/

WORKDIR /pif/bot-playground

FROM main as prod
ADD ./requirements.txt /pif/bot-playground/

# Download and install pip package
RUN pip install --upgrade pip
RUN pip install -r /pif/bot-playground/requirements.txt

#Copy file
ADD ./ /pif/bot-playground/

WORKDIR /pif/bot-playground
ENTRYPOINT python3 -u bot.py