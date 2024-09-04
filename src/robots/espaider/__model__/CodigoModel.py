from typing import Optional
from pydantic import BaseModel
from playwright.sync_api import Frame


class CodigoModel(BaseModel):
    found: bool
    codigo: Optional[str] = None
    data_cadastro: Optional[str] = None
    iframe: Optional[Frame] = None

    class Config:
        arbitrary_types_allowed = True
