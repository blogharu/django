# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt /django/
COPY . /django/
RUN apt update
RUN apt install -y libzbar0 libgl1-mesa-glx
RUN pip install --upgrade pip
RUN pip install -r requirements.txt