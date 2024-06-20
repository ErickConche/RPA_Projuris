from pydantic import BaseModel


class ZipDescompactadoModel(BaseModel):
    nome_original: str
    novo_nome_arquivo: str
