
from modules.deparaGeral.deparaGeral import DeparaGeral
from robots.admAutojur.useCases.deparas.deparas import Deparas
from robots.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class CorrecaoErrosUsuarioUseCase:
    def __init__(
        self,
        data_input: DadosEntradaFormatadosModel
    ) -> None:
        self.data_input = data_input
        self.depara = DeparaGeral()

    def execute(self)->DadosEntradaFormatadosModel:
        if self.depara.depara_estado_uf(self.data_input.uf):
            self.data_input.uf = self.depara.depara_estado_uf(self.data_input.uf)

        if self.data_input.tipo_sistema == 'PROCONConsumidorgov' or self.data_input.tipo_sistema == 'PROCON/Consumidor.gov':
            self.data_input.tipo_sistema = 'PROCON / Consumidor.gov.br'

        if self.data_input.tipo_processo == 'C.I.P':
            self.data_input.tipo_processo = 'C.I.P.'

        if len(self.data_input.data_solicitacao.split("/")[-1]) == 2:
            dia, mes, ano = self.data_input.data_solicitacao.split('/')
            if len(ano):
                ano = '20' + ano
            self.data_input.data_solicitacao =  f'{dia}/{mes}/{ano}'

        if self.data_input.arquivo_principal[-1:] == "\n":
            self.data_input.arquivo_principal = self.data_input.arquivo_principal[:-1]

        return self.data_input