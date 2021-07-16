FROM python:3.8.11-alpine

WORKDIR /code

COPY . .

RUN cd examples/shell && pip install -r requirements.txt

WORKDIR /code/examples/shell

CMD ["sh"]
