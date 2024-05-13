
import requests
from urllib.parse import urlencode
from robots.expJudAutojur.useCases.iniciandoProcessoExpAutojur.__model__.CodigoModel import InfosRequisicaoModel
from robots.expJudAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirResponsavelUseCase:
    def __init__(
        self,
        view_state: str,
        infos_requisicao: InfosRequisicaoModel,
        data_input: DadosEntradaFormatadosModel
    ) -> None:
        self.view_state = view_state
        self.infos_requisicao = infos_requisicao
        self.data_input = data_input

    def execute(self)->str:
        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "formDetalhesTarefa:responsavel:responsavel",
            "javax.faces.partial.execute": "formDetalhesTarefa:responsavel:responsavel",
            "javax.faces.partial.render": "formDetalhesTarefa:responsavel:responsavel",
            "formDetalhesTarefa:responsavel:responsavel": "formDetalhesTarefa:responsavel:responsavel",
            "formDetalhesTarefa:responsavel:responsavel_query": self.data_input.responsavel,
            "formDetalhesTarefa": "formDetalhesTarefa",
            "formDetalhesTarefa:ff-tipo-evento:cmb-tipo-evento": "1",
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_input": self.data_input.evento,
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_hinput": self.data_input.id_evento,
            "formDetalhesTarefa:data-final:datafinal_input": self.data_input.data,
            "formDetalhesTarefa:ff-prazo-interno:dataInterna_input": self.data_input.data.split()[0],
            "formDetalhesTarefa:responsavel:responsavel_input": self.data_input.responsavel,
            "formDetalhesTarefa:ff-conteudo:conteudo": "",
            "javax.faces.ViewState": self.view_state
        })

        response = requests.post(url=self.infos_requisicao.url_post, data=body, headers=self.infos_requisicao.headers)
        
        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "formDetalhesTarefa:responsavel:responsavel",
            "javax.faces.partial.execute": "formDetalhesTarefa:responsavel:responsavel",
            "javax.faces.behavior.event": "valueChange",
            "javax.faces.partial.event": "change",
            "formDetalhesTarefa:responsavel:responsavel_input": self.data_input.responsavel,
            "javax.faces.ViewState": self.view_state
        })
        response = requests.post(url=self.infos_requisicao.url_post, data=body, headers=self.infos_requisicao.headers)

        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "formDetalhesTarefa:responsavel:responsavel",
            "javax.faces.partial.execute": "formDetalhesTarefa:responsavel:responsavel",
            "javax.faces.partial.render": "formDetalhesTarefa:responsavel:responsavel formDetalhesTarefa:cmb-evento form-adicionar-tarefa:btn-salvar-criar-correlata",
            "javax.faces.behavior.event": "itemSelect",
            "javax.faces.partial.event": "itemSelect",
            "formDetalhesTarefa:responsavel:responsavel_itemSelect": self.data_input.id_responsavel,
            "formDetalhesTarefa": "formDetalhesTarefa",
            "formDetalhesTarefa:ff-tipo-evento:cmb-tipo-evento": "1",
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_input": self.data_input.evento,
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_hinput": self.data_input.id_evento,
            "formDetalhesTarefa:data-final:datafinal_input": self.data_input.data,
            "formDetalhesTarefa:ff-prazo-interno:dataInterna_input": self.data_input.data.split()[0],
            "formDetalhesTarefa:responsavel:responsavel_input": "",
            "formDetalhesTarefa:responsavel:responsavel_hinput": self.data_input.id_responsavel,
            "formDetalhesTarefa:ff-conteudo:conteudo": "",
            "javax.faces.ViewState": self.view_state
        })

        response = requests.post(url=self.infos_requisicao.url_post, data=body, headers=self.infos_requisicao.headers)

        return