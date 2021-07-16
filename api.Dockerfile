FROM python:3.8.11-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /code
RUN chown appuser:appgroup -R .

USER appuser
ADD --chown=appuser:appgroup . app

WORKDIR /code/app

RUN python -m venv venv
ENV PATH "/code/app/venv/bin:$PATH"
RUN python -m pip install --upgrade pip

RUN cd examples/api && pip install -r requirements.txt

EXPOSE 8089

WORKDIR /code/app/examples/api

CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8089", "--reload"]
