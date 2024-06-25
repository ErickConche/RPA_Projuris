from typing import Optional
from pydantic import BaseModel

class DadosCookiesModel(BaseModel):
    url: Optional[str]
    conteudo: Optional[str]
    session_cookie: Optional[str]
