import time
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.autojur.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirDadosResponsavelUseCase:
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
            self.page.locator('#panel-responsaveis\\:form-responsaveis\\:btn-edit-responsavel').click()
            time.sleep(5)
            self.page.locator('#panel-responsaveis\\:form-responsavel\\:ff-responsavel\\:ac-responsavel\\:autocomplete_input').click()
            time.sleep(1)
            self.page.locator('#panel-responsaveis\\:form-responsavel\\:ff-responsavel\\:ac-responsavel\\:autocomplete_input').type(self.data_input.nome_responsavel)
            time.sleep(3)
            self.page.locator(f'li[data-item-value="{self.data_input.id_responsavel}"]').click()
            time.sleep(2)
            self.page.locator('#panel-responsaveis\\:form-responsavel\\:ff-etapa\\:ac-etapa').click()
            time.sleep(2)
            self.page.locator('#panel-responsaveis\\:form-responsavel\\:ff-etapa\\:ac-etapa').type("Única")
            time.sleep(1)
            self.page.locator('li[data-item-label="ÚNICA"]').click()
            time.sleep(2)
            self.page.locator('#panel-responsaveis\\:form-responsavel\\:ff-btn\\:btn-add-responsavel').click()
            time.sleep(3)
            self.page.locator('#panel-responsaveis\\:form-responsavel\\:btn-salvar-responsavel').click()
            time.sleep(5)

        except Exception as error:
            message = "Erro ao inserir dados do responsável"
            self.classLogger.message(message)
            raise Exception ("Erro ao inserir dados do responsável")