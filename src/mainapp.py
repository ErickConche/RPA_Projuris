import os
import time
import warnings
from typing import List
from psycopg2 import pool
from threading import Thread
from dotenv import load_dotenv
from main_core_single import MainCoreSingle
from main_core_paralel import MainCoreParalel
from models.queues.queueExecucao import QueueExecucao
from database.Postgres import create_connect as create_con_pg

warnings.filterwarnings('ignore')
load_dotenv()

connection_pool = pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=14,
    user=os.getenv("USERRD"),
    password=os.getenv("PASSRD"),
    host=os.getenv("HOSTRD"),
    database=os.getenv("DBRD")
)


def initApp(queue: str):
    try:
        while True:
            print(f"Rodando aplicativo da fila {queue}")
            con_rd = create_con_pg(
                host=os.getenv("HOSTRD"),
                port=os.getenv("PORTRD"),
                database=os.getenv("DBRD"),
                user=os.getenv("USERRD"),
                password=os.getenv("PASSRD")
            ).get_connect()
            class_queue_execucao = QueueExecucao(con=con_rd)
            requisicoes = class_queue_execucao.buscarQueue(
                virtual_host=os.getenv("VIRTUAL_HOST"),
                queue=queue
            )
            if len(requisicoes) > 0:
                if queue == 'app-adm-autojur-joao':
                    MainCoreParalel(
                        queue=queue,
                        requisicoes=requisicoes,
                        class_queue_execucao=class_queue_execucao
                    ).init()
                else:
                    MainCoreSingle(
                        queue=queue,
                        requisicao=requisicoes[0],
                        class_queue_execucao=class_queue_execucao
                    ).init()
            else:
                time.sleep(30)
            con_rd.close()
    except Exception as error:
        print(f'Erro ao iniciar o aplicativo {queue.upper()} -> {error}')
        time.sleep(30)
        initApp(queue)


def initThreads(list_queues: List[str]):
    for queue in list_queues:
        t = Thread(target=initApp, args=(queue,))
        t.start()
        time.sleep(1)
