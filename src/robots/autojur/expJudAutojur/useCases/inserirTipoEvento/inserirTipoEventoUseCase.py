import requests
from urllib.parse import urlencode
from robots.autojur.expJudAutojur.useCases.iniciandoProcessoExpAutojur.__model__.CodigoModel import InfosRequisicaoModel


class InserirTipoEventoUseCase:
    def __init__(
        self,
        view_state: str,
        infos_requisicao: InfosRequisicaoModel
    ) -> None:
        self.view_state = view_state
        self.infos_requisicao = infos_requisicao

    def execute(self):
        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "formDetalhesTarefa:ff-tipo-evento:cmb-tipo-evento",
            "javax.faces.partial.execute": "formDetalhesTarefa:ff-tipo-evento:cmb-tipo-evento",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
            "formDetalhesTarefa:ff-tipo-evento:cmb-tipo-evento": "1",
            "javax.faces.ViewState": self.view_state
        })

        response = requests.post(url=self.infos_requisicao.url_post, data=body, headers=self.infos_requisicao.headers)
        return 