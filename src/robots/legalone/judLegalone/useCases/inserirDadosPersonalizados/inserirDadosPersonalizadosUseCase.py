import time
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirDadosPersonalizadosUseCase:
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

    def execute(self):
        try:
            self.page.locator("#NumeroDaReserva_ProcessoEntitySchema_p3812_o").click()
            time.sleep(1)
            self.page.locator("#NumeroDaReserva_ProcessoEntitySchema_p3812_o").type(self.data_input.numero_reserva)
            time.sleep(1)

            self.page.locator("#IDDoHotel_ProcessoEntitySchema_p3813_o").click()
            time.sleep(1)
            self.page.locator("#IDDoHotel_ProcessoEntitySchema_p3813_o").type(self.data_input.id_acomodacao)
            time.sleep(1)

            if self.data_input.data_citacao != '':
                self.page.query_selector('#DataDeCitacao_ProcessoEntitySchema_p3814_o').click()
                time.sleep(1)
                self.page.evaluate(f'document.querySelector("#DataDeCitacao_ProcessoEntitySchema_p3814_o").value = "{self.data_input.data_citacao}";')
                time.sleep(1)

            self.page.locator("#CausaRaizMotivacao_ProcessoEntitySchema_p3817_o_Value").click()
            time.sleep(1)
            self.page.locator("#CausaRaizMotivacao_ProcessoEntitySchema_p3817_o_Value").type("Outros")
            time.sleep(1)
            self.page.locator("#CausaRaizMotivacao_ProcessoEntitySchema_p3817_o_Value").press("Enter")
            time.sleep(3)
            elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
            elemento_dropdown.locator(f'tr[data-val-id="28"] td[data-val-field="Value"]:text("Outros")').click()
            time.sleep(3)

        except Exception as error:
            raise Exception("Erro ao inserir os dados dos outros envolvidos")