
from typing import List
from models.eventos_exp_jud.__model__.dadosEventosModel import DadosEventosModel
from models.eventos_exp_jud.useCases.buscarEventos.buscarEventosUseCase import BuscarEventosUseCase


class EventosExpJud:
    def __init__(
        self,
        con_rd
    ) -> None:
        self.con_rd = con_rd

    def buscarEventos(self)->List[DadosEventosModel]:
        return BuscarEventosUseCase(con_rd=self.con_rd).execute()