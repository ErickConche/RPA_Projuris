import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page

from modules.logger.Logger import Logger
from robots.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class VerificarDuplicidadeLitispendenciaUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger,
        tag: str
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.tag = tag

    def execute(self):
        site_response = BeautifulSoup(self.page.locator(self.tag).inner_html(), 'html.parser')
        tds = site_response.select("td")
        if self.data_input.processo == tds[2].text:
            message = "Já existe uma pasta para esse processo, verifique se não é uma duplicação."
            self.classLogger.message(message)
            raise Exception(message)
        self.page.locator(f"{self.tag} .ui-commandlink.ui-widget.btn.btn-default").click()
        time.sleep(3)
        if self.page.locator(f"{self.tag} .ui-commandlink.ui-widget.btn.btn-default").is_visible():
            self.page.locator(f"{self.tag} .ui-commandlink.ui-widget.btn.btn-default").click()
            time.sleep(3)