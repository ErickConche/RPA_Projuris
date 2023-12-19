import json
import time
import warnings
from models.cliente.cliente import Cliente
from modules.enviarPlataforma.enviarPlataforma import EnviarPlataforma
from modules.logger.Logger import Logger

from models.queues.queueExecucao import QueueExecucao
from modules.robotCore.robotCore import RobotCore
warnings.filterwarnings('ignore')
import os
from dotenv import load_dotenv
load_dotenv()
from database.Postgres import create_connect as create_con_pg
from datetime import date, timedelta, datetime
from typing import List
from threading import Thread

def main(
    json_recebido,
    task_id,
    identifier_tenant,
    queue
):
    con_rd = create_con_pg(
                host=os.getenv("HOSTRD"),
                port=os.getenv("PORTRD"),
                database=os.getenv("DBRD"),
                user=os.getenv("USERRD"),
                password=os.getenv("PASSRD")
    ).get_connect()
    try:
        class_cliente = Cliente(con=con_rd)
        cliente = class_cliente.buscarCliente(tenant=identifier_tenant)
        classLogger = Logger(hiring_id=task_id)
        data = RobotCore(
            con_rd=con_rd,
            classLogger=classLogger,
            json_recebido=json_recebido,
            task_id=task_id,
            identifier_tenant=identifier_tenant,
            cliente=cliente,
            queue=queue
        ).execute()
        EnviarPlataforma(
            tenant=identifier_tenant,
            classLogger=classLogger,
            data=data.data_return,
            task_id=task_id,
            error=data.error
        ).execute()
    except Exception as error:
        pass
    finally:
        con_rd.close()

def initApp(queue:str):
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
            if len(requisicoes)>0:
                json_recebido = json.loads(requisicoes[0]['json_recebido'])
                class_logger = Logger(hiring_id=json_recebido['TaskId'])
                message = "Inicio da aplicação "+str(datetime.now())
                class_logger.message(message=message)
                try:
                    main(
                        json_recebido=requisicoes[0]['json_recebido'],
                        task_id=json_recebido['TaskId'],
                        identifier_tenant=json_recebido['IdentifierTentant'],
                        queue=requisicoes[0]['queue']
                    )
                except Exception as error:
                    pass
                finally:
                    message = "Fim da aplicação "+str(datetime.now())
                    class_logger.message(message=message)
                    class_queue_execucao.finalizarExecQueue(requisicoes[0]['id'])
            con_rd.close()
            time.sleep(60)
    except Exception as error:
        initApp(queue)

def initThreads(list_queues: List[str]):
    for queue in list_queues:
        t = Thread(target=initApp,args=(queue,))
        t.start()
        time.sleep(1)