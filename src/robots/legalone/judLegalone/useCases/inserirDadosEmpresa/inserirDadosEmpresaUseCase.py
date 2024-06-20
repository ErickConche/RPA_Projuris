import time
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirDadosEmpresaUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.context = context

    def execute(self):
        try:
            self.page.locator("#Cliente_EnvolvidoText").click()
            time.sleep(1)
            self.page.locator("#Cliente_EnvolvidoText").type(self.data_input.empresa)
            time.sleep(1)
            self.page.locator("#Cliente_EnvolvidoText").press("Enter")
            time.sleep(3)
            elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
            elemento_dropdown.locator(f'tr[data-val-id="4036"] td[data-val-field="ContatoNome"]:text("{self.data_input.empresa}")').click()
            time.sleep(1)

            self.page.locator("#Cliente_PosicaoEnvolvidoText").click()
            time.sleep(1)
            self.page.locator("#Cliente_PosicaoEnvolvidoText").type("Réu")
            time.sleep(1)
            self.page.locator("#Cliente_PosicaoEnvolvidoText").press("Enter")
            time.sleep(3)
            elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
            elemento_dropdown.locator(f'tr[data-val-id="2"] td[data-val-field="Value"]:text("Réu")').click()
            time.sleep(1)

        except Exception as error:
            raise Exception("Erro ao inserir os dados da empresa")