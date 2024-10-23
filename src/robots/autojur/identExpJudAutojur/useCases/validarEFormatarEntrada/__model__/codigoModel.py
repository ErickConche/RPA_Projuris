from pydantic import BaseModel

class CodigoModel(BaseModel):
    processo: str
    data_expediente: str
    processo_cadastrado: str

