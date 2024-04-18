import json
import time
import warnings
import global_variables.error_ged_legalone as error_ged_legalone
from models.cliente.cliente import Cliente
from models.log_execucao.log_execucao import LogExecucao
from modules.enviarPlataforma.enviarPlataforma import EnviarPlataforma
from modules.logger.Logger import Logger

from models.queues.queueExecucao import QueueExecucao
from modules.robotCore.__model__.RobotModel import RobotModel
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
    json_recebido:str,
    task_id:str,
    identifier_tenant:str,
    queue:str,
    id_queue: int
):
    con_rd = create_con_pg(
        host=os.getenv("HOSTRD"),
        port=os.getenv("PORTRD"),
        database=os.getenv("DBRD"),
        user=os.getenv("USERRD"),
        password=os.getenv("PASSRD")
    ).get_connect()
    try:
        attemp = 0
        max_attemp = 3
        data:RobotModel = None
        while attemp < max_attemp:
            class_cliente = Cliente(con=con_rd)
            cliente = class_cliente.buscarCliente(tenant=identifier_tenant)
            classLogger = Logger(hiring_id=task_id)
            message = "Inicio da aplicação "+str(datetime.now())
            classLogger.message(message=message)
            classLogExecucao = LogExecucao(con=con_rd)
            if not data:
                data = RobotCore(
                    con_rd=con_rd,
                    classLogger=classLogger,
                    json_recebido=json_recebido,
                    task_id=task_id,
                    identifier_tenant=identifier_tenant,
                    cliente=cliente,
                    queue=queue,
                    id_queue=id_queue
                ).execute()
                if not data.error or 'autojur' in queue or (data.error and not error_ged_legalone.get_error_ged_legalone()):
                    attemp = max_attemp
        if not data.error:
            classLogExecucao.inserirLog(
                queue_execucao=queue,
                json_recebido=json.loads(json_recebido),
                json_envio=data.data_return[0]
            )
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
        message = "Fim da aplicação "+str(datetime.now())
        classLogger.message(message=message)
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
                try:
                    main(
                        json_recebido=requisicoes[0]['json_recebido'],
                        task_id=json_recebido['TaskId'],
                        identifier_tenant=json_recebido['IdentifierTentant'],
                        queue=requisicoes[0]['queue'],
                        id_queue=requisicoes[0].get("id")
                    )
                except Exception as error:
                    pass
                finally:
                    class_queue_execucao.finalizarExecQueue(requisicoes[0]['id'])
            else:
                time.sleep(60)
            con_rd.close()
    except Exception as error:
        time.sleep(60)
        initApp(queue)

def initThreads(list_queues: List[str]):
    for queue in list_queues:
        t = Thread(target=initApp,args=(queue,))
        t.start()
        time.sleep(1)