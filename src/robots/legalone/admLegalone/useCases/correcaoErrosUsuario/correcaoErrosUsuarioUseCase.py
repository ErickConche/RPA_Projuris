
from robots.legalone.admLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class CorrecaoErrosUsuarioUseCase:
    def __init__(
        self,
        data_input: DadosEntradaFormatadosModel
    ) -> None:
        self.data_input = data_input

    def execute(self) -> DadosEntradaFormatadosModel:
        if self.data_input.cidade.lower() == 'santa bárbara doeste':
            self.data_input.cidade = "Santa Bárbara d'Oeste"

        if self.data_input.tipo_processo == 'C.I.P':
            self.data_input.tipo_processo = 'C.I.P.'

        if self.data_input.tipo_sistema == 'PROCON-Consumidorgovbr':
            self.data_input.tipo_sistema = "PROCON / Consumidor.gov.br"

        if len(self.data_input.data_solicitacao.split("/")[-1]) == 2:
            dia, mes, ano = self.data_input.data_solicitacao.split('/')
            if len(ano):
                ano = '20' + ano
            self.data_input.data_solicitacao =  f'{dia}/{mes}/{ano}'

        if self.data_input.arquivo_principal[-1:] == "\n":
            self.data_input.arquivo_principal = self.data_input.arquivo_principal[:-1]

        if self.data_input.arquivos_secundarios[-1:] == "\n":
            self.data_input.arquivos_secundarios = self.data_input.arquivos_secundarios[:-1]

        return self.data_input