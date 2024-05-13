import requests

from bs4 import BeautifulSoup
from urllib.parse import urlencode
from robots.expJudAutojur.useCases.iniciandoProcessoExpAutojur.__model__.CodigoModel import InfosRequisicaoModel


class LimparResponsavelUseCase:
    def __init__(
        self,
        view_state: str,
        infos_requisicao: InfosRequisicaoModel,
        responsaveis_html: BeautifulSoup
    ) -> None:
        self.view_state = view_state
        self.responsaveis_html = responsaveis_html
        self.infos_requisicao = infos_requisicao

    def execute(self):
        for site_html in self.responsaveis_html:
            token = site_html.select("li")[0].attrs.get("data-token-value")
            body = urlencode({
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "formDetalhesTarefa:responsavel:responsavel",
                "javax.faces.partial.execute": "formDetalhesTarefa:responsavel:responsavel",
                "javax.faces.partial.render": "form-adicionar-tarefa:btn-salvar-criar-correlata",
                "javax.faces.behavior.event": "itemUnselect",
                "javax.faces.partial.event": "itemUnselect",
                "formDetalhesTarefa:responsavel:responsavel_itemUnselect": token,
                "formDetalhesTarefa:responsavel:responsavel_input": "",
                "javax.faces.ViewState": self.view_state
            })

            response = requests.post(url=self.infos_requisicao.url_post, data=body, headers=self.infos_requisicao.headers)

        return 