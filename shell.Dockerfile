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

RUN cd examples/shell && pip install -r requirements.txt

WORKDIR /code/app/examples/shell

CMD ["sh"]
