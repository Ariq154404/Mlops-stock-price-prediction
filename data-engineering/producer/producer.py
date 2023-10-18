import pika
import json
import requests
import time
max_retries = 5
retry_interval = 5
# Setup connection to RabbitMQ
RABBITMQ_HOST = "localhost"  # Default value
RABBITMQ_USER = "user"
RABBITMQ_PASSWORD = "password"

for _ in range(max_retries):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)))
        channel = connection.channel()
        channel.queue_declare(queue='stock-queue')
        # rest of your code
        break  # if connection is successful, break out of the loop
    except pika.exceptions.AMQPConnectionError:
        print(f"Failed to connect to RabbitMQ. Retrying in {retry_interval} seconds...")
        time.sleep(retry_interval)
else:
    raise Exception("Max retries reached. Could not connect to RabbitMQ.")
# connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
# channel = connection.channel()
# channel.queue_declare(queue='stock-queue')

# Fetch data from Alpha Vantage API
response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=ZCCS8Y9TXCKVHP4Q')
data = response.json()

time_series = data.get("Time Series (5min)", {})

for timestamp, stock_data in time_series.items():
    avg_price = sum(float(stock_data[key]) for key in ["1. open", "2. high", "3. low", "4. close"]) / 4.0

    message = {
        'stock_date': timestamp,
        'stock_price': avg_price
    }
    print(message)

    channel.basic_publish(exchange='', routing_key='stock-queue', body=json.dumps(message))

connection.close()
