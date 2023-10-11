FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir mysql-connector-python

CMD ["python", "db_create.py"]