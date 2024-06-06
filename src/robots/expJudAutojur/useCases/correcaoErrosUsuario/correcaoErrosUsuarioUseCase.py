
from robots.expJudAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class CorrecaoErrosUsuarioUseCase:
    def __init__(
        self,
        data_input: DadosEntradaFormatadosModel
    ) -> None:
        self.data_input = data_input

    def execute(self)->DadosEntradaFormatadosModel:
        if self.data_input.responsavel == 'Marcos Vinicius Teruel':
            self.data_input.responsavel = 'Marcos Vinicius Teruel Junior'
        if self.data_input.responsavel == 'Felipe Marques Machado':
            self.data_input.responsavel = 'Filipe Marques Machado'

        return self.data_input