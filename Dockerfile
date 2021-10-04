# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt /django/
RUN apt update
RUN apt install -y libzbar0
RUN pip install -r requirements.txt
COPY . /django/
