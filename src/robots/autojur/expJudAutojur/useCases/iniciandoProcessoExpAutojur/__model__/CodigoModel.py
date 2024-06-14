from requests import Session
from pydantic import BaseModel
from typing import List, Optional

class InfosRequisicaoModel(BaseModel):
    url: str
    url_post: str
    headers: dict
    pfdlgcid: str
    uuid_processo: str
    view_state: str
    url_processo: str

class CodigoModel(BaseModel):
    found: bool
    codigo: Optional[str] = None 