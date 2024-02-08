from typing import List, Optional
from pydantic import BaseModel

class ObjEnvolvidosModel(BaseModel):
    nome: str
    cpf_cnpj: str
    tag_objeto: str