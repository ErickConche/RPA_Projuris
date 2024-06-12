from modules.logger.Logger import Logger
from robots.autojur.useCases.listarEnvolvidos.__model__.ObjEnvolvidosModel import ObjEnvolvidosModel
from robots.autojur.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class AlterarObjetoEntradaUseCase:
    def __init__(
        self,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger,
        envolvido: ObjEnvolvidosModel
    ) -> None:
        self.data_input = data_input
        self.classLogger = classLogger
        self.envolvido = envolvido

    def execute(self):
        try:
            if self.envolvido.tag_objeto == 'nome_envolvido':
                self.data_input.nome_envolvido = self.envolvido.nome
                self.data_input.cpf_cnpj_envolvido = self.envolvido.cpf_cnpj

            elif self.envolvido.tag_objeto == 'nome_outros_envolvidos1':
                self.data_input.nome_outros_envolvidos1 = self.envolvido.nome
                self.data_input.cpf_cnpj_outros_envolvidos1 = self.envolvido.cpf_cnpj

            elif self.envolvido.tag_objeto == 'nome_outros_envolvidos2':
                self.data_input.nome_outros_envolvidos2 = self.envolvido.nome
                self.data_input.cpf_cnpj_outros_envolvidos2 = self.envolvido.cpf_cnpj

            elif self.envolvido.tag_objeto == 'nome_outros_envolvidos3':
                self.data_input.nome_outros_envolvidos3 = self.envolvido.nome
                self.data_input.cpf_cnpj_outros_envolvidos3 = self.envolvido.cpf_cnpj

            elif self.envolvido.tag_objeto == 'nome_outros_envolvidos4':
                self.data_input.nome_outros_envolvidos4 = self.envolvido.nome
                self.data_input.cpf_cnpj_outros_envolvidos4 = self.envolvido.cpf_cnpj

            elif self.envolvido.tag_objeto == 'nome_outros_envolvidos5':
                self.data_input.nome_outros_envolvidos5 = self.envolvido.nome
                self.data_input.cpf_cnpj_outros_envolvidos5 = self.envolvido.cpf_cnpj

            elif self.envolvido.tag_objeto == 'nome_outros_envolvidos6':
                self.data_input.nome_outros_envolvidos6 = self.envolvido.nome
                self.data_input.cpf_cnpj_outros_envolvidos6 = self.envolvido.cpf_cnpj

            elif self.envolvido.tag_objeto == 'nome_outros_envolvidos7':
                self.data_input.nome_outros_envolvidos7 = self.envolvido.nome
                self.data_input.cpf_cnpj_outros_envolvidos7 = self.envolvido.cpf_cnpj

            elif self.envolvido.tag_objeto == 'nome_outros_envolvidos8':
                self.data_input.nome_outros_envolvidos8 = self.envolvido.nome
                self.data_input.cpf_cnpj_outros_envolvidos8 = self.envolvido.cpf_cnpj

            elif self.envolvido.tag_objeto == 'nome_outros_envolvidos9':
                self.data_input.nome_outros_envolvidos9 = self.envolvido.nome
                self.data_input.cpf_cnpj_outros_envolvidos9 = self.envolvido.cpf_cnpj

            elif self.envolvido.tag_objeto == 'nome_outros_envolvidos10':
                self.data_input.nome_outros_envolvidos10 = self.envolvido.nome
                self.data_input.cpf_cnpj_outros_envolvidos10 = self.envolvido.cpf_cnpj
                
            return self.data_input
        except Exception as error:
            message = "Erro ao alterar Objeto de entrada dds envolvidos recebidos"
            self.classLogger.message(message)
            raise error