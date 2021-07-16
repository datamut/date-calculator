FROM python:3.8.11-alpine

WORKDIR /code

COPY . .

RUN cd examples/api && pip install -r requirements.txt

EXPOSE 8089

WORKDIR /code/examples/api

CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8089", "--reload"]
