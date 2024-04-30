
from modules.deparaGeral.useCases.deparaEstadoCapital import DeparaEstadoCapitalUseCase
from modules.deparaGeral.useCases.deparaEstadoUf import DeparaEstadoUfUseCase


class DeparaGeral:
    def __init__(self) -> None:
        pass

    def depara_estado_uf(self, estado: str):
        return DeparaEstadoUfUseCase(estado=estado).execute()
    
    def depara_estado_capital(self, uf: str):
        return DeparaEstadoCapitalUseCase(uf=uf).execute()