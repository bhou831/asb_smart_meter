import pika
import json

with open('config.json') as file:
    configuration = json.load(file)

RABBITMQ_HOST = configuration["HOST"]
QUEUE_NAME = configuration["QUEUE"]
result_lst = []

def receive_from_queue(ch, method, properties, body):
    global result_lst
    data = json.loads(body)
    # Append received data to the list
    result_lst.append(data)
    print(f"Updated data list: {result_lst}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=receive_from_queue, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()