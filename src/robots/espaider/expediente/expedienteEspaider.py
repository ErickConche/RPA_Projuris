from modules.logger.Logger import Logger
from modules.robotCore.__model__.RobotModel import RobotModel
from models.cliente.__model__.ClienteModel import ClienteModel
from robots.espaider.useCases.initRegister.initRegisterUseCase import InitRegisterUseCase

class ExpedienteEspaider:
    def __init__(
        self,
        con_rd,
        classLogger: Logger,
        json_recebido: str,
        task_id: str,
        identifier_tenant: str,
        queue: str,
        client: ClienteModel
    ) -> None:
        self.con_rd = con_rd
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.task_id = task_id
        self.identifier_tenant = identifier_tenant
        self.queue = queue
        self.client = client

    def execute(self):
        data: RobotModel = RobotModel(
            error=True,
            data_return=[]
        )

        try:
            data_return = InitRegisterUseCase(
                con_rd=self.con_rd,
                client=self.client,
                classLogger=self.classLogger,
                identifier_tenant=self.identifier_tenant,
                json_recebido=self.json_recebido,
                queue=self.queue,
                task_id=self.task_id,
                robot='Expediente'
            ).execute()

            data.error = False
            data.data_return = data_return
        except Exception as error:
            message = f"Erro: {error}"
            self.classLogger.message(message)
            data_error = [{
                "Pasta": "",
                "Processo": "SITE INDISPONÍVEL",
                "DataCadastro": "",
            }]
            data.data_return = data_error

        finally:
            return data