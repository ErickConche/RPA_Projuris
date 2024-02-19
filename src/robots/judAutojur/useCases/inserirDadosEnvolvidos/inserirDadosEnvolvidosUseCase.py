import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.judAutojur.useCases.inserirDadosEmpresa.inserirDadosEmpresaUseCase import InserirDadosEmpresaUseCase
from robots.judAutojur.useCases.inserirDadosParte.inserirDadosParteUseCase import InserirDadosParteUseCase
from robots.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

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
            InserirDadosEmpresaUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger
            ).execute()
            time.sleep(10)

            InserirDadosParteUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger
            ).execute()
            time.sleep(10)

        except Exception as error:
            raise error