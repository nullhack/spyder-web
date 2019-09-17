# AUTHOR: Eric Lopes
# DESCRIPTION: universal crawler
# BUILD: docker build -t spyderweb:local .

FROM ubuntu:19.04

RUN set -ex &&\
    apt update -y &&\
    apt upgrade -y &&\
    # installing apt dependencies
    apt install -y --no-install-recommends redis &&\
    apt install -y --no-install-recommends curl &&\
    apt install -y --no-install-recommends build-essential &&\
    apt install -y --no-install-recommends redis &&\
    apt install -y --no-install-recommends firefox-geckodriver &&\
    apt install -y --no-install-recommends libnss3 libgconf-2-4 chromium-chromedriver &&\
    apt install -y --no-install-recommends python3 python3-pip python3-dev python3-setuptools &&\
    # installing python dependencies
    pip3 install -U pip &&\
    pip3 install selenium ipython fastapi uvicorn email-validator redis hiredis redis-collections &&\
    # removing unecessary files
    apt  purge --auto-remove -y build-essential &&\
    apt autoremove -y --purge &&\
    apt clean 

WORKDIR /scripts

