FROM python:3.9-slim

WORKDIR /app

COPY producer.py /app/
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "producer.py"]
