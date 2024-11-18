from typing import Optional
from pydantic import BaseModel

class DadosEntradaFormatadosModel(BaseModel):
    username: str
    password: str
    footprint: str
    url_cookie: str
    processo: Optional[str]
    reclamacao: Optional[str]
    pessoa: Optional[str]
