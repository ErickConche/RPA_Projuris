import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.judLegalone.useCases.buscarComarca.buscarComarcaUseCase import BuscarComarcaUseCase
from robots.judLegalone.useCases.buscarComplementoComarca.buscarComplementoComarcaUseCase import BuscarComplementoComarcaUseCase
from robots.judLegalone.useCases.buscarDadosCidade.buscarDadosCidadeUseCase import BuscarDadosCidadeUseCase
from robots.judLegalone.useCases.buscarDadosUf.buscarDadosUfUseCase import BuscarDadosUfUseCase
from robots.judLegalone.useCases.buscarOrgao.buscarOrgaoUseCase import BuscarOrgaoUseCase
from robots.judLegalone.useCases.buscarVara.buscarVaraUseCase import BuscarVaraUseCase
from robots.judLegalone.useCases.deparas.deparas import Deparas
from robots.judLegalone.useCases.paginarElemento.paginarElementoUseCase import PaginarElementoUseCase
from robots.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class InserirDadosComplementaresUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger,
        context: BrowserContext,
        id_uf: int
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.context = context
        self.id_uf = id_uf

    def execute(self):
        try:
            if self.data_input.titulo == 'Indenizatória':
                self.page.locator('p:has-text("Dados complementares")').click()
                time.sleep(3)

            self.page.locator("#JusticaText").click()
            time.sleep(1)
            self.page.locator("#JusticaText").type(self.data_input.justica)
            time.sleep(3)
            self.page.locator("#JusticaText").press("Enter")
            time.sleep(3)
            elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
            elemento_dropdown.locator(f'tr[data-val-id="{Deparas.depara_justica(self.data_input.justica)}"] td[data-val-field="Value"]:text("{self.data_input.justica}")').click()
            time.sleep(5)

            info_comarca = BuscarComarcaUseCase(
                comarca=self.data_input.comarca,
                classLogger=self.classLogger,
                context=self.context,
                id_uf=self.id_uf,
                id_justica=Deparas.depara_justica(self.data_input.justica)
            ).execute()
            self.page.locator("#ForoText").click()
            time.sleep(1)
            self.page.locator("#ForoText").type(self.data_input.comarca)
            time.sleep(3)
            self.page.locator("#ForoText").press("Enter")
            time.sleep(3)
            elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
            elemento_dropdown.locator(f'tr[data-val-id="{info_comarca.get("Id")}"] td[data-val-field="Value"]:text("{info_comarca.get("Value")}")').click()
            time.sleep(3)

            if self.data_input.complemento_comarca != 'Não':
                info_complemento_comarca = BuscarComplementoComarcaUseCase(
                    classLogger=self.classLogger,
                    context=self.context,
                    complemento_comarca=self.data_input.complemento_comarca,
                    id_comarca=info_comarca.get("Id")
                ).execute()
                self.page.locator("#ComplementoForoText").click()
                time.sleep(1)
                self.page.locator("#ComplementoForoText").type(self.data_input.complemento_comarca)
                time.sleep(3)
                self.page.locator("#ComplementoForoText").press("Enter")
                time.sleep(3)
                elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
                elemento_dropdown.locator(f'tr[data-val-id="{info_complemento_comarca.get("Id")}"] td[data-val-field="Value"]:text("{info_complemento_comarca.get("Value")}")').click()
                time.sleep(3)

            if self.data_input.numero_vara!= 'Não':
                self.page.locator("#NumeroVaraTurma").click()
                time.sleep(1)
                self.page.locator("#NumeroVaraTurma").type(self.data_input.numero_vara)
                time.sleep(3)

            info_vara = BuscarVaraUseCase(
                vara=self.data_input.vara,
                classLogger=self.classLogger,
                context=self.context
            ).execute()
            self.page.locator("#VaraText").click()
            time.sleep(1)
            self.page.locator("#VaraText").type(self.data_input.vara)
            time.sleep(3)
            self.page.locator("#VaraText").press("Enter")
            time.sleep(3)
            PaginarElementoUseCase(
                page=self.page,
                classLogger=self.classLogger,
                context=self.context,
                id_elemento=info_vara.get("Id"),
                valor_elemento=info_vara.get("Value")
            ).execute()
            elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
            elemento_dropdown.locator(f'tr[data-val-id="{info_vara.get("Id")}"] td[data-val-field="Value"]:text("{info_vara.get("Value")}")').click()
            time.sleep(5)


        except Exception as error:
            raise Exception("Erro ao inserir os dados complementares")