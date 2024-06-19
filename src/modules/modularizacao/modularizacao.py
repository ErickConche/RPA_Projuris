from modules.modularizacao.useCases.modularizarDataUseCase import ModularizarData


class Modularizacao:
    def __init__(self) -> None:
        pass

    def modularizar_data(self, data_1: str, data_2: str):
        return ModularizarData(data_1, data_2).execute()