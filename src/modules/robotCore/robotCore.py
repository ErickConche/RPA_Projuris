

from logging import Logger
from models.cliente.cliente import Cliente

from modules.robotCore.__model__.RobotModel import RobotModel
from robots.admLegalone.admLegalone import AdmLegalone

class RobotCore:
    def __init__(
        self,
        con_rd,
        classLogger: Logger,
        json_recebido:str,
        task_id:str,
        identifier_tenant:str,
        cliente:Cliente,
        queue:str
    ) -> None:
        self.con_rd = con_rd
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.task_id = task_id
        self.identifier_tenant = identifier_tenant
        self.cliente = cliente
        self.queue = queue

    def execute(self)-> RobotModel:
        if self.queue == 'app-jud-legalone':
            ####TODO jud
            pass

        elif self.queue == 'app-adm-legalone':
            return AdmLegalone(
                con_rd=self.con_rd,
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                task_id=self.task_id,
                identifier_tenant=self.identifier_tenant,
                cliente=self.cliente
            ).execute()