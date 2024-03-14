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
        classLogger: Logger
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        site_response = BeautifulSoup(self.page.locator("#modal-litispendencia").inner_html(), 'html.parser')
        tds = site_response.select("td")
        if self.data_input.processo == tds[2].text:
            message = "Já existe uma pasta para esse processo, verifique se não é uma duplicação."
            self.classLogger.message(message)
            raise Exception(message)
        self.page.locator("#modal-litispendencia .ui-commandlink.ui-widget.btn.btn-default").click()
        time.sleep(3)