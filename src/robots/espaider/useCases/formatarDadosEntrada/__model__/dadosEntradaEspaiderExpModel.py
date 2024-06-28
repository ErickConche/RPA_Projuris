from pydantic import BaseModel
from typing import Optional

class DadosEntradaEspaiderExpModel(BaseModel):
    cookie_session: str
    username: str
    password: str
    data_expediente: str
    processo: str
    andamento: str
    complementos: Optional[str]
    compromisso: Optional[str]
    data_audiencia: Optional[str]
    hora_audiencia: Optional[str]