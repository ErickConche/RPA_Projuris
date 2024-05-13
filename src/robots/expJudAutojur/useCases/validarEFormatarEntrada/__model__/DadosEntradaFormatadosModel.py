from typing import List, Optional
from pydantic import BaseModel

class DadosEntradaFormatadosModel(BaseModel):
    username: str
    password: str
    footprint: str
    url_cookie: str
    cookie_session: Optional[str]
    processo: str
    evento: str
    id_evento: str = ''
    tipo_evento: str
    data: str
    data_final: str
    responsavel: str
    id_responsavel: str = ''
    arquivo: str