import pika
import mysql.connector
import json
import time
from zenml import step
import threading


class StockDatabase:

    def __init__(self, rabbitmq_host="localhost", rabbitmq_user="user", rabbitmq_password="password", mysql_host="localhost", mysql_user="root", mysql_port=3307, mysql_password="my-secret-pw", mysql_database="stocks", max_retries=5, retry_interval=5):
        self.RABBITMQ_HOST = rabbitmq_host
        self.RABBITMQ_USER = rabbitmq_user
        self.RABBITMQ_PASSWORD = rabbitmq_password
        self.MYSQL_HOST = mysql_host
        self.MYSQL_USER = mysql_user
        self.MYSQL_PORT = mysql_port
        self.MYSQL_PASSWORD = mysql_password
        self.MYSQL_DATABASE = mysql_database
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.connection = None
        self.channel = None
        self.mysql_conn = None
        self.cursor = None
        self.connect_to_rabbitmq()
        self.connect_to_mysql()

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

    def connect_to_mysql(self):
        self.mysql_conn = mysql.connector.connect(
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            user=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            database=self.MYSQL_DATABASE
        )
        self.cursor = self.mysql_conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_table (
                stock_date DATETIME PRIMARY KEY,
                stock_price DECIMAL(10,2)
            )
        """)

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        stock_date = message['stock_date']
        stock_price = message['stock_price']
        # print("sp",stock_price)
        self.cursor.execute("""
            INSERT INTO stock_table (stock_date, stock_price) 
            VALUES (%s, %s) 
            ON DUPLICATE KEY UPDATE stock_price = %s
        """, (stock_date, stock_price, stock_price))
        self.mysql_conn.commit()

    def start_consuming(self):
        self.channel.basic_consume(queue='stock-queue', on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def close_connections(self):
        if self.connection:
            self.connection.close()
        if self.mysql_conn:
            self.mysql_conn.close()
@step

def consume(status: bool) -> None:
    if not status:
        return

    def worker():
        stock_db = StockDatabase()
        stock_db.start_consuming()
        stock_db.close_connections()

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join(timeout=10)  # Wait for 3 seconds

    if thread.is_alive():
        print("Function took longer than 10 seconds. Exiting.")
        
