FROM python:3.10-slim

RUN pip install cassandra-driver

COPY src/ /app/
WORKDIR /app

CMD ["tail", "-f", "/dev/null"]