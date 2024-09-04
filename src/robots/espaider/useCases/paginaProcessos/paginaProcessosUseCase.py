import time
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)


class PaginaProcessosUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderModel,
        classLogger: Logger,
        robot: str,
        system_url: str
    ):
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.robot = robot
        self.system_url = system_url

    def execute(self):
        try:
            self.classLogger.message('Acessando a página de processos')
            self.page.locator('[data-icon="menu"]').click()
            time.sleep(2)
            self.page.locator('[id="comboModulesEdt"]').click()
            self.page.locator('li[title="Contencioso"]').click()
            time.sleep(2)
            self.page.query_selector('[tour-target="pages:container"]>a>div').click()
            return {
                "Pagina": self.page,
                "Status": True
            }
        except Exception as e:
            raise e
