from pydantic import BaseModel

class LogExecucaoModel(BaseModel):
    id: int
    queue_execucao:str
    protocolo1_recebido: str
    protocolo2_recebido: str
    protocolo_enviado: str
    data_envio: str