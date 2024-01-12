from pydantic import BaseModel

class ClienteModel(BaseModel):
    id: int
    nome: str
    tenant: str
    config_add: str