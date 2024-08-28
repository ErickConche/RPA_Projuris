from bs4 import BeautifulSoup
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.autojur.admAutojur.useCases.acessarProcesso.acessarProcessoUseCase import AcessarProcessoUseCase


class BuscarDataCadastroUseCase:
    def __init__(
        self,
        page: Page,
        classLogger: Logger,
        tr: BeautifulSoup
    ) -> None:
        self.page = page
        self.classLogger = classLogger
        self.tr = tr
    
    def execute(self):
        try:
            data_rk = self.tr.attrs.get('data-rk')
            site_html = AcessarProcessoUseCase(
                data_rk = data_rk,
                page=self.page,
                classLogger=self.classLogger
            ).execute()
            data_cad = site_html.select_one("#tabview-pasta\\:form-dados-cadastrais\\:panelAtualizacao").text
            data_cad = data_cad.split("em ")[1].split()[0]
            return data_cad
        except Exception as error:
            message = f"Erro ao buscar data de cadastro"
            self.classLogger.message(message)
            raise error