import pika
import json
import requests
import time
from zenml import step
class StockQueue:

    def __init__(self, host="localhost", user="user", password="password", max_retries=5, retry_interval=5):
        self.RABBITMQ_HOST = host
        self.RABBITMQ_USER = user
        self.RABBITMQ_PASSWORD = password
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.connection = None
        self.channel = None
        self.connect_to_rabbitmq()

    def connect_to_rabbitmq(self):
        for _ in range(self.max_retries):
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.RABBITMQ_HOST, credentials=pika.PlainCredentials(self.RABBITMQ_USER, self.RABBITMQ_PASSWORD)))
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue='stock-queue')
                break
            except pika.exceptions.AMQPConnectionError:
                print(f"Failed to connect to RabbitMQ. Retrying in {self.retry_interval} seconds...")
                time.sleep(self.retry_interval)
        else:
            raise Exception("Max retries reached. Could not connect to RabbitMQ.")

    def fetch_stock_data(self):
        response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=ZCCS8Y9TXCKVHP4Q')
        data = response.json()
        time_series = data.get("Time Series (5min)", {})
        for timestamp, stock_data in time_series.items():
            avg_price = sum(float(stock_data[key]) for key in ["1. open", "2. high", "3. low", "4. close"]) / 4.0
            message = {
                'stock_date': timestamp,
                'stock_price': avg_price
            }
            print("Message",message)
            self.channel.basic_publish(exchange='', routing_key='stock-queue', body=json.dumps(message))

    def close_connection(self):
        if self.connection:
            self.connection.close()
@step
def produce() -> bool:
    try:
        stock_queue = StockQueue()
        stock_queue.fetch_stock_data()
        stock_queue.close_connection()
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    
#if __name__ == "__main__":
    # stock_queue = StockQueue()
    # stock_queue.fetch_stock_data()
    # stock_queue.close_connection()
