import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class InserirDadosPersonalizadosUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        try:
            self.page.locator("#form-campos-personalizados\\:cp-novo-processo\\:j_idt983\\:0\\:j_idt985\\:0\\:cp-texto--").click()
            time.sleep(1)
            self.page.locator("#form-campos-personalizados\\:cp-novo-processo\\:j_idt983\\:0\\:j_idt985\\:0\\:cp-texto--").type(self.data_input.nome_procon)
            time.sleep(1)
            self.page.locator("#form-campos-personalizados\\:cp-novo-processo\\:j_idt983\\:0\\:j_idt985\\:3\\:cp-texto--").click()
            time.sleep(1)
            self.page.locator("#form-campos-personalizados\\:cp-novo-processo\\:j_idt983\\:0\\:j_idt985\\:3\\:cp-texto--").type(self.data_input.dados_reserva)
            time.sleep(1)
            self.page.locator('button[data-id="form-campos-personalizados:cp-novo-processo:j_idt983:0:j_idt985:1:cp-list--"]').click()
            time.sleep(3)
            self.page.locator('li:has-text("Digital")').click()
            time.sleep(3)
        except Exception as error:
            message = "Erro ao inserir dados personalizados"
            self.classLogger.message(message)
            raise Exception ("Erro ao inserir dados personalizados")