import time
from modules.logger.Logger import Logger
from playwright.sync_api import BrowserContext
from robots.autojur.useCases.buscarPessoa.buscarPessoaUseCase import BuscarPessoaUseCase
from robots.autojur.useCases.listarEnvolvidos.listarEnvolvidosUseCase import ListarEnvolvidosUseCase
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class VerificacaoEnvolvidosAdmUseCase:
    def __init__(
        self,
        classLogger: Logger,
        data_input: DadosEntradaFormatadosModel,
        context: BrowserContext
    ) -> None:
        self.classLogger = classLogger
        self.context = context
        self.data_input = data_input

    def execute(self):
        try:
            lista_envolvidos = ListarEnvolvidosUseCase(
                classLogger=self.classLogger,
                data_input=self.data_input,
                autojur_adm=True
            ).execute()
            for obj_envolvido in lista_envolvidos:
                envolvido = BuscarPessoaUseCase(
                    classLogger=self.classLogger,
                    context=self.context,
                    envolvido=obj_envolvido
                ).execute()
                self.data_input.cpf_cnpj_envolvido = envolvido.cpf_cnpj
                self.data_input.nome_envolvido = envolvido.nome
                time.sleep(0.5)
            return self.data_input
        except Exception as error:
            raise Exception("Erro ao verificar os dados de todos os envolvidos")