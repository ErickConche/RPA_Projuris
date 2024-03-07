
from typing import List
from models.log_execucao.useCases.definir_protocolos.definirProtocolosUseCase import DefinirProtocolosUseCase

from models.log_execucao.useCases.inserir_log.inserirLogExecucaoUseCase import InserirLogExecucaoUseCase

class LogExecucao:
    def __init__(self,con) -> None:
        self.con = con

    def inserirLog(
        self,
        queue_execucao:str,
        json_recebido: dict,
        json_envio: dict
    ):
        protocolo1_recebido, protocolo2_recebido, protocolo_enviado = DefinirProtocolosUseCase(
            queue=queue_execucao,
            json_recebido=json_recebido,
            json_enviado=json_envio
        ).execute()
        return InserirLogExecucaoUseCase(
            con=self.con,
            queue_execucao=queue_execucao,
            protocolo1_recebido=protocolo1_recebido,
            protocolo2_recebido=protocolo2_recebido,
            protocolo_enviado=protocolo_enviado
        ).execute()