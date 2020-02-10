FROM python:3.7-alpine
MAINTAINER Ebram Shehata (ebram96)

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir /recipe-app-api
WORKDIR /recipe-app-api
COPY ./src/recipe-app-api /recipe-api-app

RUN adduser -D ebram96
USER ebram96
