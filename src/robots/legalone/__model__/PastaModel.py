from typing import List, Optional
from pydantic import BaseModel

class PastaModel(BaseModel):
    found: bool
    pasta: Optional[str] = None 
    protocolo: Optional[str] = None 
    url_pasta: Optional[str] = None 
    data_cadastro: Optional[str] = None 
    url_pasta_originaria: Optional[str] = None 