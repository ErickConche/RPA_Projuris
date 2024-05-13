from typing import List
from pydantic import BaseModel
from modules.logger.Logger import Logger


class RobotModel(BaseModel):
    error: bool
    data_return: List[dict]

class RobotModelParalel(BaseModel):
    error: bool
    data_return: List[dict]
    identifier_tenant: str
    classLogger: Logger
    task_id: str
    id_requisicao: int
    json_recebido: dict

    class Config:
        arbitrary_types_allowed = True