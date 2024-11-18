from pydantic import BaseModel
from typing import Optional

class CodigoModel(BaseModel):
    status: str
    protocolo: Optional[str]



