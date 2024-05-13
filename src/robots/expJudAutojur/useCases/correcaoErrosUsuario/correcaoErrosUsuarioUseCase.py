
from robots.expJudAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class CorrecaoErrosUsuarioUseCase:
    def __init__(
        self,
        data_input: DadosEntradaFormatadosModel
    ) -> None:
        self.data_input = data_input

    def execute(self)->DadosEntradaFormatadosModel:
        return self.data_input