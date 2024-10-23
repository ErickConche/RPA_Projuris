import json
import time
import warnings
import global_variables.error_ged_legalone as error_ged_legalone
from main_core_single import MainCoreSingle
from main_core_paralel import MainCoreParalel
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
                if 'app-exp-jud' in queue:
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