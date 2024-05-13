from typing import Optional
from pydantic import BaseModel

class DadosCookiesModel(BaseModel):
    url: str
    conteudo: str
    session_cookie: Optional[str]
