from typing import Optional
from pydantic import BaseModel


class DadosEntradaTarefaFormatadosModel(BaseModel):
    username: str
    password: str
    footprint: str
    url_cookie: str
    dados_busca: str
    evento: str
    data: str
    hora: str
    responsavel: str
    conteudo: str
    cookie_session: Optional[str]
