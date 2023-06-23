FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y sudo software-properties-common curl wget git

RUN adduser --disabled-password --gecos '' dev
RUN adduser dev sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER dev

WORKDIR /home/dev

RUN curl -s https://raw.githubusercontent.com/henrikwilhelmsen/hw-config-cli/main/scripts/bootstrap.sh | bash

CMD /bin/bash