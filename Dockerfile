FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir -p speaq/api

ADD ./requirements.txt /speaq/api
RUN pip install -r /speaq/api/requirements.txt

ADD . /speaq/api
ADD .kaggle /root/.kaggle

WORKDIR /speaq/api/src


