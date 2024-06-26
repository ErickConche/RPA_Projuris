from playwright.sync_api import BrowserContext, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
import time
from robots.espaider.useCases.formularioGeral.formularioGeralUseCase import (
    FormularioGeralUseCase)
from robots.espaider.useCases.formularioPartesProcesso.formularioPartesProcessoUseCase import (
    FormularioPartesProcessoUseCase)


class CriarCodigoUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderModel,
        classLogger: Logger,
        context: BrowserContext,
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.context = context

    def execute(self):
        try:
            form_response = FormularioGeralUseCase(
                page=self.page,
                classLogger=self.classLogger,
                data_input=self.data_input,
            ).execute()
            
            if not form_response:
                raise Exception("Erro ao preencher dados gerais")
            
            form_parts_response = FormularioPartesProcessoUseCase(
                page=self.page,
                classLogger=self.classLogger,
                data_input=self.data_input
            ).execute()

            if not form_parts_response:
                raise Exception("Erro ao preencher dados complementares")

            return form_response
        except Exception as e:
            self.classLogger.message(e.args[0])
            raise e
