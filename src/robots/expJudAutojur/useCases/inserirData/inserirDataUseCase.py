
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from robots.expJudAutojur.useCases.iniciandoProcessoExpAutojur.__model__.CodigoModel import InfosRequisicaoModel
from robots.expJudAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirDataUseCase:
    def __init__(
        self,
        view_state: str,
        infos_requisicao: InfosRequisicaoModel,
        data_input: DadosEntradaFormatadosModel,
        id_responsavel_ativo: str
    ) -> None:
        self.view_state = view_state
        self.infos_requisicao = infos_requisicao
        self.data_input = data_input
        self.id_responsavel_ativo = id_responsavel_ativo

    def execute(self):
        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "formDetalhesTarefa:data-final:datafinal",
            "javax.faces.partial.execute": "formDetalhesTarefa:data-final:datafinal",
            "javax.faces.partial.render": "formDetalhesTarefa:ff-prazo-interno",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
            "formDetalhesTarefa": "formDetalhesTarefa",
            "formDetalhesTarefa:ff-tipo-evento:cmb-tipo-evento": "1",
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_input": self.data_input.evento,
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_hinput": self.data_input.id_evento,
            "formDetalhesTarefa:data-final:datafinal_input": self.data_input.data,
            "formDetalhesTarefa:ff-prazo-interno:dataInterna_input": "",
            "formDetalhesTarefa:responsavel:responsavel_input": "",
            "formDetalhesTarefa:ff-conteudo:conteudo": "",
            "javax.faces.ViewState": self.view_state
        })

        response = requests.post(url=self.infos_requisicao.url_post, data=body, headers=self.infos_requisicao.headers)

        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "formDetalhesTarefa:ff-prazo-interno:dataInterna",
            "javax.faces.partial.execute": "formDetalhesTarefa:ff-prazo-interno:dataInterna",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
            "formDetalhesTarefa": "formDetalhesTarefa",
            "formDetalhesTarefa:ff-tipo-evento:cmb-tipo-evento": "1",
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_input": self.data_input.evento,
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_hinput": self.data_input.id_evento,
            "formDetalhesTarefa:data-final:datafinal_input": self.data_input.data,
            "formDetalhesTarefa:ff-prazo-interno:dataInterna_input": self.data_input.data.split()[0],
            "formDetalhesTarefa:responsavel:responsavel_input": "",
            "formDetalhesTarefa:ff-conteudo:conteudo": "",
            "javax.faces.ViewState": self.view_state
        })

        response = requests.post(url=self.infos_requisicao.url_post, data=body, headers=self.infos_requisicao.headers)
        return 