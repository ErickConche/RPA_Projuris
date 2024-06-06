from typing import Optional
from pydantic import BaseModel

class DadosEventosModel(BaseModel):
    nome_evento: str
    id_evento: str
    usa_hora: bool
