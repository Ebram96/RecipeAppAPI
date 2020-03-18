FROM python:3.7-alpine
MAINTAINER Ebram Shehata (ebram96)

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /RecipeAppAPI
WORKDIR /RecipeAppAPI
COPY ./src/RecipeAppAPI /RecipeAppAPI

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D ebram96

RUN chown -R ebram96:ebram96 /vol/
RUN chown -R 755 /vol/web/

USER ebram96
