from typing import List
from pydantic import BaseModel

class RobotModel(BaseModel):
    error: bool
    data_return: List[dict]