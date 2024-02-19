import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class InserirDadosComentariosUseCAse:
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
            mensagem = self.data_input.arquivo_principal
            if self.data_input.houve_expedicao != 'Não':
                mensagem = "A citação foi expedida. \n\n"+ mensagem
            self.page.locator("#comments-panel\\:btn-comentar").click()
            time.sleep(5)
            modal = self.page.locator("#modal-add-comentario")
            modal.locator("#comments-dialog\\:form-cad-comentario\\:ff-descricao\\:txt-descricao_editor").click()
            time.sleep(1)
            modal.locator("#comments-dialog\\:form-cad-comentario\\:ff-descricao\\:txt-descricao_editor").type(mensagem)
            time.sleep(3)
            modal.locator("#comments-dialog\\:form-cad-comentario\\:j_idt1344").click()
            time.sleep(5)

        except Exception as error:
            message = "Erro ao inserir dados do comentario"
            self.classLogger.message(message)
            raise Exception ("Erro ao inserir dados do comentario")