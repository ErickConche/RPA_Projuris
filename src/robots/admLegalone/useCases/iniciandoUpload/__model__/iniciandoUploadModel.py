

from pydantic import BaseModel


class IniciandoUploadModel(BaseModel):
    id_pasta: str
    id_vinculo: str
    pasta: str
    request_verification_token: str
    nome_arquivo_server: str
    nome_arquivo: str