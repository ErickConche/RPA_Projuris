import time
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.admLegalone.useCases.deparas.deparas import Deparas
from robots.legalone.useCases.buscarDadosUf.buscarDadosUfUseCase import BuscarDadosUfUseCase
from robots.legalone.useCases.buscarDadosCidade.buscarDadosCidadeUseCase import BuscarDadosCidadeUseCase


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
            time.sleep(3)
            self.page.locator(f'tr[data-val-id="{Deparas.depara_sistema(self.tipo_sistema)}"] td[data-val-field="Value"]:text("{self.tipo_sistema}")').click()
            time.sleep(3)

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
            time.sleep(3)
            self.page.locator(f'tr[data-val-id="{info_uf.get("Id")}"] td[data-val-field="UFText"]:text("{info_uf.get("UFText")}")').click()
            time.sleep(3)


            try:
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
                time.sleep(3)
                self.page.locator(f'tr[data-val-id="{info_cidade.get("Id")}"] td[data-val-field="Value"]:text("{info_cidade.get("Value")}")').click()
                time.sleep(3)
            except Exception as error:
                message = "Erro ao buscar cidade. Continuará a execução porém sem a informação da cidade"
                self.classLogger.message(message)

        except Exception as error:
            raise Exception("Erro ao inserir dados principais no formulario de criação")
        