import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from modules.logger.Logger import Logger


class BuscarProcessoUseCase:
    def __init__(
        self,
        view_state: str,
        headers: dict,
        url: str,
        processo: str,
        classLogger: Logger
    ) -> None:
        self.view_state = view_state
        self.headers = headers
        self.url = url
        self.classLogger = classLogger
        self.processo = processo

    def execute(self):
        try:
            body = urlencode({
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "form-pesquisa:componente-pesquisa:cmb-campo-pesquisa-rapida",
                "javax.faces.partial.execute": f"orm-pesquisa:componente-pesquisa:campo",
                "javax.faces.partial.render": "form-pesquisa:componente-pesquisa:operador form-pesquisa:componente-pesquisa:valor form-pesquisa:componente-pesquisa:campo",
                "javax.faces.behavior.event": "change",
                "javax.faces.partial.event": "change",
                "form-pesquisa": "form-pesquisa",
                "javax.faces.ViewState": self.view_state,
                "form-pesquisa:componente-pesquisa:cmb-campo-pesquisa-rapida": "43",
                "form-pesquisa:componente-pesquisa:j_idt301": "1",
                "form-pesquisa:componente-pesquisa:txt-conteudo": "",
                "form-pesquisa:tipo-proc": "4",
                "form-pesquisa:cmb-ordenacao": "-",
                "form-pesquisa:radio-status": "ATIVO"
            })

            response = requests.post(url=self.url,  data=body, headers=self.headers)

            body = urlencode({
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "form-pesquisa:componente-pesquisa:btn-pesquisar",
                "javax.faces.partial.execute": "form-pesquisa:componente-pesquisa:pesquisa-rapida form-pesquisa list-processos:tabela",
                "javax.faces.partial.render": "list-processos btnAcoes:btnAddTarefa btnAcoes:btn-editar btnAcoes:gerarFinanceiro form-pesquisa:componente-pesquisa:pesquisa-rapida",
                "form-pesquisa:componente-pesquisa:btn-pesquisar": "form-pesquisa:componente-pesquisa:btn-pesquisar",
                "form-pesquisa": "form-pesquisa",
                "javax.faces.ViewState": self.view_state,
                "form-pesquisa:componente-pesquisa:cmb-campo-pesquisa-rapida": "80",
                "form-pesquisa:componente-pesquisa:j_idt301": "1",
                "form-pesquisa:componente-pesquisa:txt-conteudo": self.processo,
                "form-pesquisa:tipo-proc": "4",
                "form-pesquisa:cmb-ordenacao": "-",
                "form-pesquisa:radio-status": "ATIVO"
            })

            response = requests.post(url=self.url,  data=body, headers=self.headers)

            site_html = BeautifulSoup(BeautifulSoup(response.text, 'html.parser').select("update")[4].next, 'html.parser')
            trs = site_html.select_one("#list-processos\\:tabela_data").select("tr")
            return trs
        except Exception as error:
            message = f"Erro ao buscar o processo"
            self.classLogger.message(message)
            raise error
    