FROM python:3.9.16-alpine3.16 as main

WORKDIR /pif

#Install python 3
RUN apk add --update --no-cache py3-pip

RUN apk add py3-virtualenv 
RUN apk add python3-dev build-base py3-numpy py3-dbus py3-cairo py3-gobject3 py3-dbus

#Install other platform requirement
RUN apk add libffi-dev ffmpeg libsm libxext cairo-dev gobject-introspection-dev linux-headers dbus-libs dbus-glib-dev

# Install utility
RUN apk update && \
    apk add pkgconfig &&\
    pip install -U setuptools wheel

FROM main as dev

# Install utility
RUN apk update && \
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
ENTRYPOINT python -u bot.py