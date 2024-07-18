import time
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.judLegalone.useCases.deparas.deparas import Deparas
from robots.legalone.useCases.buscarOrgao.buscarOrgaoUseCase import BuscarOrgaoUseCase
from robots.legalone.useCases.buscarDadosUf.buscarDadosUfUseCase import BuscarDadosUfUseCase
from robots.legalone.useCases.buscarDadosCidade.buscarDadosCidadeUseCase import BuscarDadosCidadeUseCase
from robots.legalone.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirDadosAreaPrincipalUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.context = context

    def execute(self)->int:
        try:
            if self.data_input.titulo == 'Indenizatória':
                id_titulo = 11
                valor_titulo  = 'Indenizatória'
            elif self.data_input.titulo == 'Reclamação Pré-Processual':
                id_titulo = 37
                valor_titulo  = 'Reclamação Pré-Processual'
            elif self.data_input.titulo == 'Cumprimento de Sentença':
                id_titulo = 6
                valor_titulo  = 'Cumprimento de Sentença'
            elif self.data_input.titulo == 'Carta Precatória':
                id_titulo = 8
                valor_titulo  = 'Carta Precatória'
            else:
                message = "Titulo invalido"
                self.classLogger.message(message)
                raise Exception(message)
            self.page.locator('#LookupTitulo .lookup-button.lookup-modal-button').click()
            time.sleep(5)
            elemento_modal = self.page.locator('.lookup-modal')
            elemento_envolvido = elemento_modal.locator('[id^="lookup"][id$="_dropdown"]')
            elemento_envolvido.locator('input[class="search"]').click()
            time.sleep(3)
            elemento_envolvido.locator('input[class="search"]').type(valor_titulo)
            time.sleep(2)
            elemento_envolvido.locator('input[class="search"]').press('Enter')
            time.sleep(5)
            elemento_modal.locator(f'tr[data-val-id="{id_titulo}"] td[data-val-field="Value"]:text("{valor_titulo}")').click()
            time.sleep(5)

            self.page.locator("#NumeroCNJ").click()
            time.sleep(1)
            self.page.locator("#NumeroCNJ").type(self.data_input.processo)
            time.sleep(1)

            self.page.query_selector('#DataDistribuicao').click()
            time.sleep(1)
            self.page.evaluate(f'document.querySelector("#DataDistribuicao").value = "{self.data_input.data_distribuicao}";')
            time.sleep(1)

            self.page.query_selector('#TipoAcaoText').click()
            time.sleep(1)
            self.page.query_selector('#TipoAcaoText').type(valor_titulo)
            time.sleep(1)
            self.page.locator('#lookup_tipoacao .lookup-button.lookup-filter').click()
            time.sleep(2)
            elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
            if valor_titulo == 'Cumprimento de Sentença':
                valor_titulo = 'Cumprimento de Sentença.'
            if valor_titulo == 'Carta Precatória':
                valor_titulo = 'Carta Precatória.'
            elemento_dropdown.locator(f'tr[data-val-id="{Deparas.depara_acao(valor_titulo)}"] td[data-val-field="Value"]:text("{valor_titulo}")').click()
            time.sleep(2)

            if id_titulo == 11 or id_titulo == 37:
                if id_titulo != 37:
                    self.page.query_selector('#NaturezaText').click()
                    time.sleep(1)
                    self.page.query_selector('#NaturezaText').type(self.data_input.natureza)
                    time.sleep(1)
                    self.page.locator('#lookup_natureza .lookup-button.lookup-filter').click()
                    time.sleep(2)
                    elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
                    elemento_dropdown.locator(f'tr[data-val-id="{Deparas.depara_natureza(self.data_input.natureza)}"] td[data-val-field="Value"]:text("{self.data_input.natureza}")').click()
                    time.sleep(2)

                    self.page.query_selector('#ProcedimentoText').click()
                    time.sleep(1)
                    self.page.query_selector('#ProcedimentoText').type(self.data_input.procedimento)
                    time.sleep(1)
                    self.page.locator('#lookup_Procedimento .lookup-button.lookup-filter').click()
                    time.sleep(2)
                    elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
                    elemento_dropdown.locator(f'tr[data-val-id="{Deparas.depara_procedimento(self.data_input.procedimento)}"] td[data-val-field="Value"]:text("{self.data_input.procedimento}")').click()
                    time.sleep(2)

                self.page.query_selector('#FaseText').click()
                time.sleep(1)
                self.page.query_selector('#FaseText').type(self.data_input.fase)
                time.sleep(1)
                self.page.locator('#lookup_fase .lookup-button.lookup-filter').click()
                time.sleep(2)
                elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
                elemento_dropdown.locator(f'tr[data-val-id="{Deparas.depara_fase(self.data_input.fase)}"] td[data-val-field="Value"]:text("{self.data_input.fase}")').click()
                time.sleep(2)

            info_orgao = BuscarOrgaoUseCase(
                orgao_julgador=self.data_input.orgao_julgador,
                classLogger=self.classLogger,
                context=self.context
            ).execute()
            self.page.query_selector('#OrgaoText').click()
            time.sleep(1)
            self.page.query_selector('#OrgaoText').type(self.data_input.orgao_julgador)
            time.sleep(1)
            self.page.locator('#lookup_orgao .lookup-button.lookup-filter').click()
            time.sleep(2)
            elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
            elemento_dropdown.locator(f'tr[data-val-id="{info_orgao.get("Id")}"] td[data-val-field="Value"]:text("{info_orgao.get("Value")}")').click()
            time.sleep(2)

            info_uf = BuscarDadosUfUseCase(
                uf=self.data_input.uf,
                classLogger=self.classLogger,
                context=self.context
            ).execute()
            self.page.query_selector('#UFText').click()
            time.sleep(1)
            self.page.query_selector('#UFText').type(self.data_input.uf)
            time.sleep(1)
            self.page.locator('#lookup_UF .lookup-button.lookup-filter').click()
            time.sleep(2)
            elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
            elemento_dropdown.locator(f'tr[data-val-id="{info_uf.get("Id")}"] td[data-val-field="UFText"]:text("{info_uf.get("UFText")}")').click()
            time.sleep(2)

            try:
                info_cidade = BuscarDadosCidadeUseCase(
                    id_uf=info_uf.get("Id"),
                    cidade=self.data_input.cidade,
                    classLogger=self.classLogger,
                    context=self.context
                ).execute()
                self.page.query_selector('#CidadeText').click()
                time.sleep(1)
                self.page.query_selector('#CidadeText').type(self.data_input.cidade)
                time.sleep(1)
                self.page.locator('#lookup_cidade .lookup-button.lookup-filter').click()
                time.sleep(5)
                elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
                elemento_dropdown.locator(f'tr[data-val-id="{info_cidade.get("Id")}"] td[data-val-field="Value"]:text("{info_cidade.get("Value")}")').click()
                time.sleep(5)
                return info_uf.get("Id"), info_cidade.get("Id")
            except Exception as error:
                message = "Erro ao buscar cidade. Continuará a execução porém sem a informação da cidade"
                self.classLogger.message(message)

            return info_uf.get("Id"), None
        except Exception as error:
            raise Exception("Erro ao inserir os dados na area principal do cadastro")