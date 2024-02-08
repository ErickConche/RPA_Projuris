from typing import List, Optional
from pydantic import BaseModel

class PastaModel(BaseModel):
    found: bool
    pasta: Optional[str] = None 
    url_pasta: Optional[str] = None 
    protocolo: Optional[str] = None 