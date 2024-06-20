import time
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.judLegalone.useCases.deparas.deparas import Deparas
from robots.legalone.useCases.buscarVara.buscarVaraUseCase import BuscarVaraUseCase
from robots.legalone.useCases.buscarComarca.buscarComarcaUseCase import BuscarComarcaUseCase
from robots.legalone.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


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
            if self.data_input.titulo == 'Indenizatória' or self.data_input.titulo == 'Reclamação Pré-Processual':
                self.page.locator('p:has-text("Dados complementares")').click()
                time.sleep(3)
            justica = self.data_input.justica
            self.page.locator("#JusticaText").click()
            time.sleep(1)
            self.page.locator("#JusticaText").type(justica)
            time.sleep(3)
            self.page.locator("#JusticaText").press("Enter")
            time.sleep(3)
            elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
            elemento_dropdown.locator(f'tr[data-val-id="{Deparas.depara_justica(justica)}"] td[data-val-field="Value"]:text("{justica}")').click()
            time.sleep(5)

            list_info_comarca = BuscarComarcaUseCase(
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
            for info_comarca in list_info_comarca:
                 if elemento_dropdown.locator(f'tr[data-val-id="{info_comarca.get("Id")}"] td[data-val-field="Value"]:text("{info_comarca.get("Value")}")').is_visible():
                     elemento_dropdown.locator(f'tr[data-val-id="{info_comarca.get("Id")}"] td[data-val-field="Value"]:text("{info_comarca.get("Value")}")').click()
                     break
            time.sleep(3)

            if self.data_input.vara != '':
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
                elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
                elemento_dropdown.locator(f'tr[data-val-id="{info_vara.get("Id")}"] td[data-val-field="Value"]:text("{info_vara.get("Value")}")').click()
                time.sleep(3)


        except Exception as error:
            raise Exception("Erro ao inserir os dados complementares")