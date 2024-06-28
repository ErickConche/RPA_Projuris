from logging import Logger
from models.cliente.cliente import Cliente
from robots.autojur.judAutojur.judAutojur import JudAutojur
from robots.autojur.admAutojur.admAutojur import AdmAutoJur
from modules.robotCore.__model__.RobotModel import RobotModel
from robots.legalone.judLegalone.judLegalone import judLegalone
from robots.legalone.admLegalone.admLegalone import AdmLegalone
from robots.espaider.civeis.civeisEspaider import CiveisEspaider
from robots.espaider.trabalhista.trabalhistaEspaider import TrabalhistaEspaider
from robots.espaider.expediente.expedienteEspaider import ExpedienteEspaider

class RobotCore:
    def __init__(
        self,
        con_rd,
        classLogger: Logger,
        json_recebido:str,
        task_id:str,
        identifier_tenant:str,
        cliente:Cliente,
        queue:str,
        id_queue: int
    ) -> None:
        self.con_rd = con_rd
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.task_id = task_id
        self.identifier_tenant = identifier_tenant
        self.cliente = cliente
        self.queue = queue
        self.id_queue = id_queue

    def execute(self)-> RobotModel:
        if 'app-jud-legalone' in self.queue:
            return judLegalone(
                con_rd=self.con_rd,
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                task_id=self.task_id,
                identifier_tenant=self.identifier_tenant,
                cliente=self.cliente,
                id_queue=self.id_queue
            ).execute()
        
        if 'app-jud-autojur' in self.queue:
            return JudAutojur(
                con_rd=self.con_rd,
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                task_id=self.task_id,
                identifier_tenant=self.identifier_tenant,
                cliente=self.cliente,
                id_queue=self.id_queue
            ).execute()

        elif 'app-adm-legalone' in self.queue:
            return AdmLegalone(
                con_rd=self.con_rd,
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                task_id=self.task_id,
                identifier_tenant=self.identifier_tenant,
                cliente=self.cliente,
                id_queue=self.id_queue
            ).execute()
        
        elif 'app-adm-autojur' in self.queue:
            return AdmAutoJur(
                con_rd=self.con_rd,
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                task_id=self.task_id,
                identifier_tenant=self.identifier_tenant,
                cliente=self.cliente,
                id_queue=self.id_queue
            ).execute()
        
        elif 'app-civeis-espaider' in self.queue:
            return CiveisEspaider(
                con_rd=self.con_rd,
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                task_id=self.task_id,
                identifier_tenant=self.identifier_tenant,
                queue=self.queue,
                client=self.cliente
            ).execute()

        elif 'app-trabalhista-espaider' in self.queue:
            return TrabalhistaEspaider(
                con_rd=self.con_rd,
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                task_id=self.task_id,
                identifier_tenant=self.identifier_tenant,
                queue=self.queue,
                client=self.cliente
            ).execute()

        elif 'app-expediente-espaider' in self.queue:
            return ExpedienteEspaider(
                con_rd=self.con_rd,
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                task_id=self.task_id,
                identifier_tenant=self.identifier_tenant,
                queue=self.queue,
                client=self.cliente
            ).execute()