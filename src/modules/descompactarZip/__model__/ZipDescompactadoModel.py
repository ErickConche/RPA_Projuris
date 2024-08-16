from pydantic import BaseModel


class ZipDescompactadoModel(BaseModel):
    nome_original: str
    novo_nome_arquivo: str
    nome_original_sem_format: str
