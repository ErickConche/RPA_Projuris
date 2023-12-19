import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger

class InserirDadosEmpresaUseCase:
    def __init__(
        self,
        page: Page,
        empresa:str,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.empresa = empresa
        self.classLogger = classLogger

    def execute(self):
        try:
            elemento_envolvido = self.page.locator('[id^="Clientes_"][id$="__EnvolvidoText"]')
            id_do_cliente_envolvido = elemento_envolvido.get_attribute('id').replace("Clientes_","").replace("__EnvolvidoText","")
            self.page.query_selector(f'#Clientes_{id_do_cliente_envolvido}__EnvolvidoText').click()
            time.sleep(5)
            self.page.query_selector(f'#Clientes_{id_do_cliente_envolvido}__EnvolvidoText').type(self.empresa)
            time.sleep(5)
            elemento_envolvido = self.page.locator(f'#Clientes_{id_do_cliente_envolvido}__lookup_envolvido')
            elemento_envolvido.locator('.lookup-button.lookup-filter').click()
            time.sleep(14)
            self.page.locator(f'tr[data-val-id="4036"]').click() ### Criar depara
            time.sleep(5)
        except Exception as error:
            raise Exception("Erro ao inserir dados da empresa no formulario de criação")