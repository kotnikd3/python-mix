FROM python:3.11-slim-buster

WORKDIR /python-mix

COPY . ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
