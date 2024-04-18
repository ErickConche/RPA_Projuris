import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.admAutojur.useCases.inserirDadosAutoridade.inserirDadosAutoridadeUseCase import InserirDadosAutoridadeUseCase
from robots.admAutojur.useCases.inserirDadosEmpresa.inserirDadosEmpresaUseCase import InserirDadosEmpresaUseCase
from robots.admAutojur.useCases.inserirDadosParte.inserirDadosParteUseCase import InserirDadosParteUseCase
from robots.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class InserirDadosEnvolvidosUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        try:
            self.classLogger.message("Inserindo dados da parte")
            InserirDadosParteUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger
            ).execute()
            time.sleep(3)

            self.classLogger.message("Inserindo dados da autoridade")
            InserirDadosAutoridadeUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger
            ).execute()
            time.sleep(3)

            self.classLogger.message("Inserindo dados da empresa")
            InserirDadosEmpresaUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger
            ).execute()
            time.sleep(3)

        except Exception as error:
            raise error