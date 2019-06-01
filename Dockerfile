FROM python:3.7.0

WORKDIR /comfort_transport
ENV HOME /comfort_transport

RUN apt-get update && apt-get install -y --no-install-recommends \
           emacs

RUN pip install --upgrade pip setuptools 
RUN pip install --upgrade pip 

RUN pip install -q flask pandas numpy requests emacs