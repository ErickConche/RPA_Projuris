import os
import time
import pika
import json
from typing import List
from models.queues.queueExecucao import QueueExecucao
from database.Postgres import create_connect as create_con_pg


def callback(ch, method, properties, body):
    try:
        json_body = json.loads(body)
        queue = method.routing_key
        # Validando dados
        if "TaskId" not in json_body \
            or "IdentifierTentant" not in json_body \
                or "Fields" not in json_body:
            return

        con_rd = create_con_pg(host=os.getenv("HOSTRD"),
                               port=os.getenv("PORTRD"),
                               database=os.getenv("DBRD"),
                               user=os.getenv("USERRD"),
                               password=os.getenv("PASSRD")).get_connect()
        QueueExecucao(con=con_rd).iniciarExecQueue(
            json_rec=json.dumps(json_body),
            virtual_host=os.getenv("VIRTUAL_HOST"),
            queue=queue)
        con_rd.close()
    except Exception as error:
        print(f'Erro no Callback -> {str(error)}')
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def initServer(list_queues: List[str]):
    try:
        server_address = os.environ.get('RABBIT_CONNECTION')
        connection = pika.BlockingConnection(pika.URLParameters(server_address))
        channel = connection.channel()
        for queue_name in list_queues:
            channel.queue_declare(queue=queue_name, durable=True)
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
            channel.basic_qos(prefetch_count=1)
        print("Iniciou os consumidores")
        channel.start_consuming()
    except Exception as error:
        print(f'Erro ao buscar informações das filas -> {error}')
        time.sleep(30)
        initServer(list_queues)
