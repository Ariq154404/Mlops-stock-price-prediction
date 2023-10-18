import pika
import mysql.connector
import json
import time
max_retries = 5
retry_interval = 5
# Setup connection to RabbitMQ
RABBITMQ_HOST = "localhost"  # Default value
RABBITMQ_USER = "user"
RABBITMQ_PASSWORD = "password"
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PORT = 3307
MYSQL_PASSWORD = "my-secret-pw"
MYSQL_DATABASE = "stocks"
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
# Setup connection to RabbitMQ
# connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
# channel = connection.channel()
# channel.queue_declare(queue='stock-queue')

# Setup MySQL connection
conn = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_table (
        stock_date DATETIME PRIMARY KEY,
        stock_price DECIMAL(10,2)
    )
""")

def callback(ch, method, properties, body):
    message = json.loads(body)
    stock_date = message['stock_date']
    stock_price = message['stock_price']
    print("sp",stock_price)
    cursor.execute("""
        INSERT INTO stock_table (stock_date, stock_price) 
        VALUES (%s, %s) 
        ON DUPLICATE KEY UPDATE stock_price = %s
    """, (stock_date, stock_price, stock_price))
    cursor.execute("SELECT * FROM stock_table ORDER BY stock_date DESC LIMIT 2")
    top_10_records = cursor.fetchall()
    print("\nTop 10 latest records:")
    for record in top_10_records:
        print(record)
    conn.commit()

channel.basic_consume(queue='stock-queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
