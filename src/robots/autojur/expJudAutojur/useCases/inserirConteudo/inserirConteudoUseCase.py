import requests
from urllib.parse import urlencode
from robots.autojur.expJudAutojur.useCases.iniciandoProcessoExpAutojur.__model__.CodigoModel import InfosRequisicaoModel
from robots.autojur.expJudAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirConteudoUseCase:
    def __init__(
        self,
        view_state: str,
        infos_requisicao: InfosRequisicaoModel,
        data_input: DadosEntradaFormatadosModel
    ) -> None:
        self.view_state = view_state
        self.infos_requisicao = infos_requisicao
        self.data_input = data_input

    def execute(self):
        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "formDetalhesTarefa:ff-conteudo:conteudo",
            "javax.faces.partial.execute": "formDetalhesTarefa:ff-conteudo:conteudo",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
            "formDetalhesTarefa:ff-conteudo:conteudo": self.data_input.arquivo,
            "javax.faces.ViewState": self.view_state
        })

        response = requests.post(url=self.infos_requisicao.url_post, data=body, headers=self.infos_requisicao.headers)

        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "form-adicionar-tarefa:btn-salvar",
            "javax.faces.partial.execute": "formModeloTarefa form-associar formDetalhesTarefa form-adicionar-colaboradores form-adicionar-observadores form-adicionar-participantes form-adicionar-tarefa:btn-salvar",
            "form-adicionar-tarefa:btn-salvar": "form-adicionar-tarefa:btn-salvar",
            "formModeloTarefa": "formModeloTarefa",
            "formModeloTarefa:modelo-tarefa": "TAREFA",
            "form-associar": "form-associar",
            "formDetalhesTarefa": "formDetalhesTarefa",
            "formDetalhesTarefa:ff-tipo-evento:cmb-tipo-evento": "1",
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_input": self.data_input.evento,
            "formDetalhesTarefa:cmb-evento:ac-evento:ac-evento_hinput": self.data_input.id_evento,
            "formDetalhesTarefa:data-final:datafinal_input": self.data_input.data,
            "formDetalhesTarefa:ff-prazo-interno:dataInterna_input": self.data_input.data.split()[0],
            "formDetalhesTarefa:responsavel:responsavel_input": "",
            "formDetalhesTarefa:responsavel:responsavel_hinput": self.data_input.id_responsavel,
            "formDetalhesTarefa:ff-conteudo:conteudo": self.data_input.arquivo,
            "form-adicionar-colaboradores": "form-adicionar-colaboradores",
            "form-adicionar-colaboradores:colaboradores:colaborador_input": "",
            "form-adicionar-colaboradores:colaboradores:colaborador_hinput": "",
            "form-adicionar-observadores": "form-adicionar-observadores",
            "form-adicionar-observadores:observadores:observador_input": "",
            "form-adicionar-observadores:observadores:observador_hinput": "",
            "form-adicionar-participantes": "form-adicionar-participantes",
            "javax.faces.ViewState": self.view_state,
            "form-adicionar-participantes:participantes:participante_input": "",
            "form-adicionar-participantes:participantes:participante_hinput": ""
        })

        response = requests.post(url=self.infos_requisicao.url_post, data=body, headers=self.infos_requisicao.headers)
        return 