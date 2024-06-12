from typing import List, Optional
from pydantic import BaseModel

class CodigoModel(BaseModel):
    found: bool
    codigo: Optional[str] = None 
    data_cadastro: Optional[str] = None 
