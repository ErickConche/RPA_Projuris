from modules.validacao.useCases.validarHoraUseCase import ValidarHoraUseCase


class Validacao:
    def __init__(self) -> None:
        pass

    def validar_hora(self, hora: str):
        return ValidarHoraUseCase(hora=hora).execute()