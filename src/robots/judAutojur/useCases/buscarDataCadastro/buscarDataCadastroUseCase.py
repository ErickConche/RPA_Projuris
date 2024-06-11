from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from robots.judAutojur.useCases.acessarProcesso.acessarProcessoUseCase import AcessarProcessoUseCase


class BuscarDataCadastroUseCase:
    def __init__(
        self,
        view_state: str,
        headers: dict,
        url: str,
        classLogger: Logger,
        tr: BeautifulSoup
    ) -> None:
        self.view_state = view_state
        self.headers = headers
        self.url = url
        self.classLogger = classLogger
        self.tr = tr
    
    def execute(self):
        try:
            data_rk = self.tr.attrs.get("data-rk")
            site_html = AcessarProcessoUseCase(
                view_state=self.view_state,
                headers=self.headers,
                url=self.url,
                data_rk=data_rk,
                classLogger=self.classLogger
            ).execute()
            data_cad = site_html.select_one("#tabview-pasta\\:form-dados-cadastrais\\:panelAtualizacao").text
            data_cad = data_cad.split("em ")[1].split()[0]
            return data_cad
        except Exception as error:
            message = f"Erro ao buscar data de cadastro"
            self.classLogger.message(message)
            raise error