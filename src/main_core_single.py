import os
import json
import warnings
from datetime import datetime
from dotenv import load_dotenv
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from modules.robotCore.robotCore import RobotCore
from models.queues.queueExecucao import QueueExecucao
from models.log_execucao.log_execucao import LogExecucao
from database.Postgres import create_connect as create_con_pg
from modules.robotCore.__model__.RobotModel import RobotModel
from modules.enviarPlataforma.enviarPlataforma import EnviarPlataforma
warnings.filterwarnings('ignore')
load_dotenv()


class MainCoreSingle:
    def __init__(
        self,
        queue: str,
        requisicao: dict,
        class_queue_execucao: QueueExecucao
    ) -> None:
        self.queue = queue
        self.requisicao = requisicao
        self.class_queue_execucao = class_queue_execucao

    def main(
        self,
        json_recebido: str,
        task_id: str,
        identifier_tenant: str,
        queue: str,
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
            data: RobotModel = None
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
        except (Exception) as error:
            classLogger.message(str(error))
        finally:
            message = "Fim da aplicação "+str(datetime.now())
            classLogger.message(message=message)
            con_rd.close()

    def init(self):
        json_recebido = json.loads(self.requisicao['json_recebido'])
        try:
            self.main(
                json_recebido=self.requisicao['json_recebido'],
                task_id=json_recebido['TaskId'],
                identifier_tenant=json_recebido['IdentifierTentant'],
                queue=self.queue,
                id_queue=self.requisicao.get("id")
            )
        except Exception as error:
            print(f'Erro no Main Core Single -> {error}')
            pass
        finally:
            self.class_queue_execucao.finalizarExecQueue(self.requisicao['id'])
