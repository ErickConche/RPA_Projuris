import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.admLegalone.useCases.buscarDadosCidade.buscarDadosCidadeUseCase import BuscarDadosCidadeUseCase
from robots.admLegalone.useCases.buscarDadosUf.buscarDadosUfUseCase import BuscarDadosUfUseCase
from robots.admLegalone.useCases.deparas.deparas import Deparas


class InserirDadosPrincipaisUseCase:
    def __init__(
        self,
        page: Page,
        tipo_sistema:str,
        data_solicitacao: str,
        uf:str,
        cidade: str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.page = page
        self.tipo_sistema = tipo_sistema
        self.data_solicitacao = data_solicitacao
        self.uf = uf
        self.cidade = cidade
        self.classLogger = classLogger
        self.context = context

    def execute(self):
        try:
            self.page.query_selector('#TipoText').click()
            time.sleep(1)
            self.page.query_selector('#TipoText').type(self.tipo_sistema)
            time.sleep(1)
            self.page.locator('#lookupTipo .lookup-button.lookup-filter').click()
            time.sleep(5)
            self.page.locator(f'tr[data-val-id="{Deparas.depara_sistema(self.tipo_sistema)}"] td[data-val-field="Value"]:text("{self.tipo_sistema}")').click()
            time.sleep(5)

            self.page.query_selector('#DtSolicitacao').click()
            time.sleep(1)
            self.page.evaluate(f'document.querySelector("#DtSolicitacao").value = "{self.data_solicitacao}";')
            time.sleep(1)

            info_uf = BuscarDadosUfUseCase(
                uf=self.uf,
                classLogger=self.classLogger,
                context=self.context
            ).execute()
            self.page.query_selector('#UFText').click()
            time.sleep(1)
            self.page.query_selector('#UFText').type(self.uf)
            time.sleep(1)
            self.page.locator('#lookup_uf .lookup-button.lookup-filter').click()
            time.sleep(5)
            self.page.locator(f'tr[data-val-id="{info_uf.get("Id")}"] td[data-val-field="UFText"]:text("{self.uf}")').click()
            time.sleep(5)

            info_cidade = BuscarDadosCidadeUseCase(
                id_uf=info_uf.get("Id"),
                cidade=self.cidade,
                classLogger=self.classLogger,
                context=self.context
            ).execute()
            self.page.query_selector('#CidadeText').click()
            time.sleep(1)
            self.page.query_selector('#CidadeText').type(self.cidade)
            time.sleep(1)
            self.page.locator('#LookupCidade .lookup-button.lookup-filter').click()
            time.sleep(5)
            self.page.locator(f'tr[data-val-id="{info_cidade.get("Id")}"] td[data-val-field="Value"]:text("{self.cidade}")').click()
            time.sleep(5)

        except Exception as error:
            raise Exception("Erro ao inserir dados principais no formulario de criação")
        