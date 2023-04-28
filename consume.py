import pika
import json
from msg import send_msg

with open('config.json') as file:
    configuration = json.load(file)

RABBITMQ_HOST = configuration["HOST"]
QUEUE_NAME = configuration["QUEUE"]
result_lst = []
power_lst = []
on_duration = 0

def monitor(power_lst):
    global on_duration
    for i in range(len(power_lst)):
        if power_lst[i] > 5:
            on_duration += 1
            if on_duration > 400:
                print("\n"*3, "Fridge Door Open, Msg sent", "\n"*3)
                send_msg()
        else:
            on_duration = 0

def receive_from_queue(ch, method, properties, body):
    global result_lst
    data = json.loads(body)
    # Append received data to the list
    result_lst.append(data)
    power_lst.append(data['power'])
    print(f"Updated power list: {power_lst}")
    monitor(power_lst)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

channel.basic_consume(queue=QUEUE_NAME, on_message_callback=receive_from_queue, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()