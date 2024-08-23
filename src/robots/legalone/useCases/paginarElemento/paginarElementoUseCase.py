import time
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext


class PaginarElementoUseCase:
    def __init__(
        self,
        page: Page,
        classLogger: Logger,
        context: BrowserContext,
        id_elemento: int,
        valor_elemento: str,
        valor_elemento_doc: str = '',
        data_val_field: str = 'Value',
        data_val_field_doc: str = 'Value'
    ) -> None:
        self.page = page
        self.classLogger = classLogger
        self.context = context
        self.id_elemento = id_elemento
        self.valor_elemento = valor_elemento
        self.data_val_field = data_val_field
        self.data_val_field_doc = data_val_field_doc
        self.valor_elemento_doc = valor_elemento_doc

    def execute(self):
        try:
            time.sleep(5)
            elemento = self.page.locator('.lookup-dropdown[style*="display: block"]')
            site_html = BeautifulSoup(elemento.inner_html(), 'html.parser')
            qtde_paginas = int(site_html.select_one(".paginator-page-count").text)
            pagina_atual = 1
            while pagina_atual <= qtde_paginas:
                if self.page.locator(f'tr[data-val-id="{self.id_elemento}"] td[data-val-field="{self.data_val_field}"]:text("{self.valor_elemento}")').is_visible():
                    return True
                if self.page.locator(f'tr[data-val-id="{self.id_elemento}"] td[data-val-field="{self.data_val_field_doc}"]:text("{self.valor_elemento_doc}")').is_visible():
                    return True
                pagina_atual += 1
                elemento.locator(".paginator-next").click()
                time.sleep(5)

            raise Exception("Erro ao fazer paginação")

        except Exception as error:
            message = "Erro ao fazer paginação"
            self.classLogger.message(message)
            raise error
