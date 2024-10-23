from typing import List
from pydantic import BaseModel

class DadosEntradaFormatadosModel(BaseModel):
    username: str
    password: str
    footprint: str
    url_cookie: str
    processo: str
    data_expediente: str
    tipo_expediente: str