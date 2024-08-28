import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page
from modules.logger.Logger import Logger

class AcessarProcessoUseCase:
    def __init__(
        self,
        page: Page,
        data_rk: str,
        classLogger: Logger
    ) -> None:
        self.data_rk = data_rk
        self.page = page
        self.classLogger = classLogger

    def execute(self):
        try:
            self.page.query_selector(f'[data-rk="{self.data_rk}"]').dblclick()
            self.page.wait_for_selector('[href="#tabview-pasta:tab-dados-cadastrais"]')
            self.page.query_selector('[href="#tabview-pasta:tab-dados-cadastrais"]').click()
            time.sleep(3)
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            if not site_html.select_one("#tabview-pasta\\:form-dados-cadastrais"):
                raise Exception("Erro ao acessar processo")
            return site_html
        except Exception as error:
            message = f"Erro ao acessar processo"
            self.classLogger.message(message)
            raise error
    