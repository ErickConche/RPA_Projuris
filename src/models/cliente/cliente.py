
from typing import List
from models.cliente.__model__.ClienteModel import ClienteModel
from models.cliente.useCases.buscarCliente.buscarClienteUseCase import BuscarClienteUseCase


class Cliente:
    def __init__(self,con) -> None:
        self.con = con

    def buscarCliente(self,tenant:str)->ClienteModel:
        return BuscarClienteUseCase(
            con=self.con,
            tenant=tenant
        ).execute()