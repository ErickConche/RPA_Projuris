import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from modules.logger.Logger import Logger


class AcessarProcessoUseCase:
    def __init__(
        self,
        view_state: str,
        headers: dict,
        url: str,
        data_rk: str,
        classLogger: Logger
    ) -> None:
        self.view_state = view_state
        self.headers = headers
        self.url = url
        self.data_rk = data_rk
        self.classLogger = classLogger

    def execute(self):
        try:
            attemp = 0 
            max_attemp = 3
            while attemp < max_attemp:
                body = urlencode({
                    "javax.faces.partial.ajax": "true",
                    "javax.faces.source": "list-processos:tabela",
                    "javax.faces.partial.execute": "list-processos:tabela",
                    "javax.faces.partial.render": "detalhes includes form-pesquisa:pg-layout-grid-body",
                    "javax.faces.behavior.event": "rowDblselect",
                    "javax.faces.partial.event": "rowDblselect",
                    "list-processos:tabela_instantSelectedRowKey": self.data_rk,
                    "list-processos:tabela_rppDD": "20",
                    "list-processos:tabela_selection": self.data_rk,
                    "javax.faces.ViewState": self.view_state
                })

                response = requests.post(url=self.url, data=body, headers=self.headers)

                body = urlencode({
                    "javax.faces.partial.ajax": "true",
                    "javax.faces.source": "tabview-pasta",
                    "javax.faces.partial.execute": "tabview-pasta",
                    "javax.faces.partial.render": "tabview-pasta",
                    "javax.faces.behavior.event": "tabChange",
                    "javax.faces.partial.event": "tabChange",
                    "tabview-pasta_contentLoad": "true",
                    "tabview-pasta_newTab": "tabview-pasta:tab-dados-cadastrais",
                    "tabview-pasta_tabindex": "2",
                    "tabview-pasta:form-timeline-pasta": "tabview-pasta:form-timeline-pasta",
                    "javax.faces.ViewState": self.view_state,
                    "tabview-pasta_activeIndex": "1",
                    "tabview-pasta_scrollState": "0",
                })

                response = requests.post(url=self.url, data=body, headers=self.headers)

                site_html = BeautifulSoup(BeautifulSoup(response.text, 'html.parser').select("update")[0].next, 'html.parser')

                if site_html.select_one("#tabview-pasta\\:form-dados-cadastrais"):
                    return site_html
                attemp += 1
                time.sleep(1)
            raise Exception("Erro ao acessar processo")
        except Exception as error:
            message = f"Erro ao acessar processo"
            self.classLogger.message(message)
            raise error
    