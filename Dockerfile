FROM python:3.7-alpine
MAINTAINER Ebram Shehata (ebram96)

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir /RecipeAppAPI
WORKDIR /RecipeAppAPI
COPY ./src/RecipeAppAPI /RecipeAppAPI

RUN adduser -D ebram96
#RUN chown ebram96:ebram96 -R /RecipeAppAPI/
USER ebram96
