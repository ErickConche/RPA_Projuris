import json
from modules.logger.Logger import Logger

class ValidarDadosEntradaExpUseCase:
    def __init__(
        self,
        classLogger: Logger,
        json_recebido: str
    ) -> None:
        self.classLogger = classLogger
        self.json_recebido = json_recebido

    def execute(self) -> bool:
        message = "Iniciando validação dos campos de entrada"
        self.classLogger.message(message)
        json_recebido: dict = json.loads(self.json_recebido)
        fields: dict = json_recebido.get("Fields")
        credentials: dict = json_recebido.get('Credentials')
        
        if not credentials.get("Username") or not credentials.get("Password"):
            raise Exception("Dados de login incorretos")
        
        if not fields.get("Processo"):
            raise Exception("Informe o número do processo")

        if not fields.get("DataExpediente"):
            raise Exception("Informe a data do expediente")

        if not fields.get("Andamento"):
            raise Exception("Informe o andamento")

        if fields.get("Compromisso") and not fields.get("DataAudiencia"):
            raise Exception("Informe a data de audiência")

        if fields.get("Compromisso") and not fields.get("HorarioAudiencia"):
            raise Exception("Informe o horário de audiência")