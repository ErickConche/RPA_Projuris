from typing import List
from modules.robotCore.__model__.RobotModel import RobotModelParalel
from robots.autojur.expJudAutojur.expJudAutojur import ExpJudAutojur


class RobotCoreParalel:
    def __init__(
        self,
        queue,
        con_rd,
        requisicoes,
    ) -> None:
        self.con_rd = con_rd
        self.requisicoes = requisicoes
        self.queue = queue

    def execute(self)-> List[RobotModelParalel]:
        if 'app-exp-jud-autojur' in self.queue:
            return ExpJudAutojur(
                con_rd=self.con_rd,
                requisicoes=self.requisicoes,
                queue=self.queue
            ).execute()