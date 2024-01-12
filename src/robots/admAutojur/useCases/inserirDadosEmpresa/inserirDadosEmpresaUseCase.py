import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class InserirDadosEmpresaUseCase:
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
            self.page.locator("#painel-envolvidos\\:form-principais-envolvidos\\:panel-envolvido-principal\\:btn-adicionar-pessoa-vazio").click()
            time.sleep(5)
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            url_iframe = f"https://baz.autojur.com.br{site_html.select_one('iframe').attrs.get('src')}"
            frame = self.page.frame(url=url_iframe)

            frame.fill('#form-pesquisa-pessoa\\:componente-pesquisa-pessoa\\:txt-conteudo',self.data_input.empresa)
            time.sleep(1)
            frame.locator("#form-pesquisa-pessoa\\:componente-pesquisa-pessoa\\:btn-pesquisar").click()
            time.sleep(5)
            frame.locator(f'tr[data-rk="23666"]').click()
            time.sleep(1)
            frame.locator("#form-pesquisa-pessoa\\:btn-selecionar").click()
            time.sleep(5)

            self.page.locator("#j_idt1248\\:form-envolvidos\\:ff-qualificacao\\:autocomplete_input").click()
            time.sleep(1)
            self.page.locator("#j_idt1248\\:form-envolvidos\\:ff-qualificacao\\:autocomplete_input").type(self.data_input.qualificacao_empresa)
            time.sleep(1)

            self.page.locator("#j_idt1248\\:form-envolvidos\\:btn-salvar-envolvido").click()
            time.sleep(5)

            popup = self.page.locator("#modal-litispendencia").is_visible()
            if popup:
                self.page.locator('#modal-litispendencia button:has-text("Fechar")').click()
                time.sleep(5)
            
        except Exception as erro:
            raise Exception("Erro ao inserir dados da empresa")