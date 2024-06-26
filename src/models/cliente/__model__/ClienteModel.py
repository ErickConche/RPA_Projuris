from pydantic import BaseModel
from typing import Optional

class ClienteModel(BaseModel):
    id: int
    nome: str
    tenant: str
    config_add: str
    base_url: Optional[str]