import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger

class InserirDadosObservacaoUseCase:
    def __init__(
        self,
        page: Page,
        observacoes:str,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.observacoes = observacoes
        self.classLogger = classLogger

    def execute(self):
        try:
            self.page.locator('p[class="panel-title"] >> text=Observações').click()
            time.sleep(5)
            self.page.query_selector('#Observacao').click()
            time.sleep(1)
            self.page.query_selector('#Observacao').type(self.observacoes)
            time.sleep(10)
        except Exception as error:
            raise Exception("Erro ao inserir dados de observacao no formulario de criação")