
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from robots.expJudAutojur.useCases.iniciandoProcessoExpAutojur.__model__.CodigoModel import InfosRequisicaoModel
from robots.expJudAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirEventoUseCase:
    def __init__(
        self,
        view_state: str,
        infos_requisicao: InfosRequisicaoModel,
        data_input: DadosEntradaFormatadosModel
    ) -> None:
        self.view_state = view_state
        self.infos_requisicao = infos_requisicao
        self.data_input = data_input
        self.data_hoje = datetime.today().strftime("%d/%m/%Y")

    def execute(self)->str:
        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento",
            "javax.faces.partial.execute": "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento",
            "javax.faces.partial.render": "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento",
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento": "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento",
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_query": self.data_input.evento,
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_dynamicload": "true",
            "formDetalhesTarefa": "formDetalhesTarefa",
            "javax.faces.ViewState": self.view_state,
            "formDetalhesTarefa:ff-tipo-evento:cmb-tipo-evento": "1",
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_input": self.data_input.evento,
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_hinput": self.data_input.evento,
            "formDetalhesTarefa:ff-publico:rd-publico": "false",
            "formDetalhesTarefa:ff-local:pac-input": "",
            "formDetalhesTarefa:ff-lote:cmb-lotes": "0",
            "formDetalhesTarefa:ff-data-inicio:datainicio_input": str(self.data_hoje),
            "formDetalhesTarefa:data-final:datafinal_input": "",
            "formDetalhesTarefa:ff-duracao:j_idt132_input": "00:30",
            "formDetalhesTarefa:ff-prazo-interno:dataInterna_input": "",
            "formDetalhesTarefa:ff-tag-livre:j_idt140:autocomplete-tag_input": "",
            "formDetalhesTarefa:responsavel:responsavel_input": "",
            "formDetalhesTarefa:ff-conteudo:conteudo": ""
        })

        response = requests.post(url=self.infos_requisicao.url_post, data=body, headers=self.infos_requisicao.headers)

        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento",
            "javax.faces.partial.execute": "formDetalhesTarefa",
            "javax.faces.behavior.event": "itemSelect",
            "javax.faces.partial.event": "itemSelect",
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_itemSelect": self.data_input.id_evento,
            "formDetalhesTarefa": "formDetalhesTarefa",
            "javax.faces.ViewState": self.view_state,
            "formDetalhesTarefa:ff-tipo-evento:cmb-tipo-evento": "1",
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_input": self.data_input.evento,
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_hinput":  self.data_input.id_evento,
            "formDetalhesTarefa:ff-publico:rd-publico": "false",
            "formDetalhesTarefa:ff-local:pac-input": "",
            "formDetalhesTarefa:ff-lote:cmb-lotes": "0",
            "formDetalhesTarefa:ff-data-inicio:datainicio_input": str(self.data_hoje),
            "formDetalhesTarefa:data-final:datafinal_input": "",
            "formDetalhesTarefa:ff-duracao:j_idt132_input": "00:30",
            "formDetalhesTarefa:ff-prazo-interno:dataInterna_input": "",
            "formDetalhesTarefa:ff-tag-livre:j_idt140:autocomplete-tag_input": "",
            "formDetalhesTarefa:responsavel:responsavel_input": "",
            "formDetalhesTarefa:ff-conteudo:conteudo": ""
        })

        response = requests.post(url=self.infos_requisicao.url_post, data=body, headers=self.infos_requisicao.headers)
        return response.text