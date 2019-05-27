FROM python:3.7.0

WORKDIR /comfort_transport
ENV HOME /comfort_transport

RUN pip install --upgrade pip setuptools 
RUN pip install --upgrade pip 

RUN pip install -q Flask pandas numpy requests