from typing import List
from pydantic import BaseModel

class DadosEntradaFormatadosModel(BaseModel):
    username: str
    password: str
    tipo_sistema: str
    uf: str
    cidade: str
    data_solicitacao: str
    empresa: str
    posicao_envolvido: str
    nome_envolvido: str
    cpf_cnpj_envolvido: str
    tipo_envolvido: str
    observacoes: str
    id_acomodacao: str
    numero_reserva: str
    nome_procon: str
    numero_reclamacao:str
    tipo_reclamacao: str
    tipo_processo: str
    dados_reserva: str
    arquivo_principal: str
    arquivos_secundarios: str
