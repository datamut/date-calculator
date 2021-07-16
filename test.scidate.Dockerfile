FROM python:3.8.11-alpine

WORKDIR /code

COPY scidate scidate

WORKDIR /code/scidate

RUN pip install -r requirements_test.txt

RUN pytest scidate/tests --cov=scidate
