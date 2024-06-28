from playwright.sync_api import BrowserContext, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderExpModel import (
    DadosEntradaEspaiderExpModel)
from modules.logger.Logger import Logger
from robots.espaider.useCases.andamento.andamentoUseCase import AndamentoUseCase

class CriarCodigoExpUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderExpModel,
        classLogger: Logger,
        context: BrowserContext,
        robot: str
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.context = context
        self.robot = robot

    def execute(self):
        try:
            return AndamentoUseCase(
                page=self.page,
                classLogger=self.classLogger,
                data_input=self.data_input,
                robot=self.robot
            ).execute()
        except Exception as e:
            raise e