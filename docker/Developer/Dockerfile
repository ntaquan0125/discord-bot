FROM --platform=linux/amd64 ubuntu:20.04
WORKDIR /pif

# Install python3.9
RUN apt update && \
    apt -y install software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt -y install python3.9 && \
    apt -y install libcairo2-dev

# Set default python3.9
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Install ssh, git, pip, venv, sshpass, nano
RUN apt update && \
    apt-get -y install git openssh-client python3-pip python3.9-dev python3.9-venv sshpass openssh-server nano tmux &&\
    pip install -U black

# Install ping
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Create virtual environments
ADD ./requirements.txt /pif/bot-playground/
RUN pip install --upgrade pip
RUN pip install -r /pif/bot-playground/requirements.txt

WORKDIR /pif/bot-playground