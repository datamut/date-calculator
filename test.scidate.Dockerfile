FROM python:3.8.11-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /code
RUN chown appuser:appgroup -R .

USER appuser

COPY --chown=appuser:appgroup scidate scidate
WORKDIR /code/scidate

RUN python -m venv venv
ENV PATH "/code/scidate/venv/bin:$PATH"
RUN python -m pip install --upgrade pip

WORKDIR /code/scidate

RUN pip install -r requirements_test.txt

CMD ["pytest", "scidate/tests", "--cov=scidate"]
