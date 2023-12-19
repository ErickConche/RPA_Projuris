from pydantic import BaseModel

class ClienteModel(BaseModel):
    nome: str
    tenant: str
    config_add: str