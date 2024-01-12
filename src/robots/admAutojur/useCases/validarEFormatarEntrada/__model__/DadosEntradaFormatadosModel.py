from typing import List
from pydantic import BaseModel

class DadosEntradaFormatadosModel(BaseModel):
    username: str
    password: str
    footprint: str
    url_cookie: str
    numero_reclamacao:str
    pasta: str
    data_solicitacao: str
    uf: str
    cidade: str
    tipo_processo: str
    tipo_extrajudicial: str
    situacao: str
    empresa: str
    qualificacao_empresa: str
    nome_envolvido: str
    tipo_envolvido: str
    cpf_cnpj_envolvido: str
    qualificacao_envolvido: str
    tipo_sistema: str
    qualificacao_sistema: str
    nome_procon: str
    tipo_reclamacao: str
    dados_reserva: str
    arquivo_principal: str
    observacoes: str