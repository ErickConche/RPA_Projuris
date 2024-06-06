import os
import json
import warnings
from typing import List
from datetime import datetime
from dotenv import load_dotenv

from modules.robotCore.robotCoreParalel import RobotCoreParalel
warnings.filterwarnings('ignore')
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from modules.robotCore.robotCore import RobotCore
from models.queues.queueExecucao import QueueExecucao
from models.log_execucao.log_execucao import LogExecucao
from database.Postgres import create_connect as create_con_pg
from modules.robotCore.__model__.RobotModel import RobotModelParalel
import global_variables.error_ged_legalone as error_ged_legalone
from modules.enviarPlataforma.enviarPlataforma import EnviarPlataforma
load_dotenv()

class MainCoreParalel:
    def __init__(
        self,
        queue: str,
        requisicoes: List[dict], 
        class_queue_execucao: QueueExecucao
    ) -> None:
        self.queue = queue
        self.requisicoes = requisicoes
        self.class_queue_execucao = class_queue_execucao

    def init(self):
        con_rd = create_con_pg(
            host=os.getenv("HOSTRD"),
            port=os.getenv("PORTRD"),
            database=os.getenv("DBRD"),
            user=os.getenv("USERRD"),
            password=os.getenv("PASSRD")
        ).get_connect()
        try:
            results: List[RobotModelParalel] = None
            results = RobotCoreParalel(
                con_rd=con_rd,
                requisicoes=self.requisicoes,
                queue=self.queue
            ).execute()
            classLogExecucao = LogExecucao(con=con_rd)
            for result in results:
                EnviarPlataforma(
                    tenant=result.identifier_tenant,
                    classLogger=result.classLogger,
                    data=result.data_return,
                    task_id=result.task_id,
                    error=result.error
                ).execute()
                if not result.error:
                    classLogExecucao.inserirLog(
                        queue_execucao=self.queue,
                        json_recebido=result.json_recebido,
                        json_envio=result.data_return[0]
                    )
                self.class_queue_execucao.finalizarExecQueue(result.id_requisicao)
        except Exception as error:
            pass
        finally:
            con_rd.close()