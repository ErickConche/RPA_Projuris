import requests
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from robots.autojur.expJudAutojur.useCases.inserirData.inserirDataUseCase import InserirDataUseCase
from robots.autojur.expJudAutojur.useCases.inserirEvento.inserirEventoUseCase import InserirEventoUseCase
from robots.autojur.expJudAutojur.useCases.iniciandoProcessoExpAutojur.__model__.CodigoModel import CodigoModel
from robots.autojur.expJudAutojur.useCases.inserirConteudo.inserirConteudoUseCase import InserirConteudoUseCase
from robots.autojur.expJudAutojur.useCases.inserirTipoEvento.inserirTipoEventoUseCase import InserirTipoEventoUseCase
from robots.autojur.expJudAutojur.useCases.limparResponsavel.limparResponsavelUseCase import LimparResponsavelUseCase
from robots.autojur.expJudAutojur.useCases.inserirResponsavel.inserirResponsavelUseCase import InserirResponsavelUseCase
from robots.autojur.expJudAutojur.useCases.iniciandoProcessoExpAutojur.__model__.CodigoModel import InfosRequisicaoModel
from robots.autojur.expJudAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class CriarTarefaUseCase:
    def __init__(
        self,
        data_input: DadosEntradaFormatadosModel,
        infos_requisicao: InfosRequisicaoModel,
        classLogger: Logger
    ) -> None:
        self.data_input = data_input
        self.classLogger = classLogger
        self.infos_requisicao = infos_requisicao

    def execute(self)->CodigoModel:
        response = requests.get(url=self.infos_requisicao.url, headers=self.infos_requisicao.headers)

        site_html = BeautifulSoup(response.text, 'html.parser')

        view_state = site_html.select_one("#formModeloTarefa").find('input', {'name': 'javax.faces.ViewState'}).attrs.get('value')
        
        InserirTipoEventoUseCase(
            view_state=view_state,
            infos_requisicao=self.infos_requisicao
        ).execute()

        response_text = InserirEventoUseCase(
            view_state=view_state,
            infos_requisicao=self.infos_requisicao,
            data_input=self.data_input
        ).execute()

        site_html = BeautifulSoup(BeautifulSoup(response_text, 'html.parser').select("update")[0].next, 'html.parser')

        InserirDataUseCase(
            view_state=view_state,
            infos_requisicao=self.infos_requisicao,
            data_input=self.data_input,
            id_responsavel_ativo=site_html.select("#formDetalhesTarefa\\:responsavel\\:responsavel")[0].select("li")[0].attrs.get("data-token-value")
        ).execute()

        if len(site_html.select("#formDetalhesTarefa\\:responsavel\\:responsavel")[0].select("li")) > 1:
            LimparResponsavelUseCase(
                view_state=view_state,
                infos_requisicao=self.infos_requisicao,
                responsaveis_html=site_html.select("#formDetalhesTarefa\\:responsavel\\:responsavel")
            ).execute()

        InserirResponsavelUseCase(
            view_state=view_state,
            infos_requisicao=self.infos_requisicao,
            data_input=self.data_input
        ).execute()

        InserirConteudoUseCase(
            view_state=view_state,
            infos_requisicao=self.infos_requisicao,
            data_input=self.data_input
        ).execute()

        return