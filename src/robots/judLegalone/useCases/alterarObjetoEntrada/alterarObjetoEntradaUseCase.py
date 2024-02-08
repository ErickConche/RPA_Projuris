from modules.logger.Logger import Logger
from robots.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class AlterarObjetoEntradaUseCase:
    def __init__(
        self,
        data_input: DadosEntradaFormatadosModel,
        valor: str,
        classLogger: Logger,
        chave: str
    ) -> None:
        self.data_input = data_input
        self.valor = valor
        self.chave = chave
        self.classLogger = classLogger

    def execute(self):
        try:
            if self.chave == 'nome_envolvido':
                self.data_input.nome_envolvido = self.valor

            elif self.chave == 'nome_outros_envolvidos1':
                self.data_input.nome_outros_envolvidos1 = self.valor

            elif self.chave == 'nome_outros_envolvidos2':
                self.data_input.nome_outros_envolvidos2 = self.valor

            elif self.chave == 'nome_outros_envolvidos3':
                self.data_input.nome_outros_envolvidos3 = self.valor

            elif self.chave == 'nome_outros_envolvidos4':
                self.data_input.nome_outros_envolvidos4 = self.valor

            elif self.chave == 'nome_outros_envolvidos5':
                self.data_input.nome_outros_envolvidos5 = self.valor

            elif self.chave == 'nome_outros_envolvidos6':
                self.data_input.nome_outros_envolvidos6 = self.valor

            elif self.chave == 'nome_outros_envolvidos7':
                self.data_input.nome_outros_envolvidos7 = self.valor

            elif self.chave == 'nome_outros_envolvidos8':
                self.data_input.nome_outros_envolvidos8 = self.valor

            elif self.chave == 'nome_outros_envolvidos9':
                self.data_input.nome_outros_envolvidos9 = self.valor

            elif self.chave == 'nome_outros_envolvidos10':
                self.data_input.nome_outros_envolvidos10 = self.valor
                
            return self.data_input
        except Exception as error:
            message = "Erro ao alterar Objeto de entrada dds envolvidos recebidos"
            self.classLogger.message(message)
            raise error