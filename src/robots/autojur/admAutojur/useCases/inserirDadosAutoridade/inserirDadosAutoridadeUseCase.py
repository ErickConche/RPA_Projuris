import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.autojur.admAutojur.useCases.deparas.deparas import Deparas
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirDadosAutoridadeUseCase:
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
            self.page.locator('a[aria-label="Adicionar Autoridade"]').click()
            time.sleep(5)

            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            url_iframe = f"https://baz.autojur.com.br{site_html.select_one('iframe').attrs.get('src')}"
            frame = self.page.frame(url=url_iframe)

            frame.fill('#form-pesquisa-pessoa\\:componente-pesquisa-pessoa\\:txt-conteudo',self.data_input.tipo_sistema)
            time.sleep(1)
            frame.locator("#form-pesquisa-pessoa\\:componente-pesquisa-pessoa\\:btn-pesquisar").click()
            time.sleep(5)

            frame.locator(f'tr[data-rk="{Deparas.depara_autoridade(self.data_input.tipo_sistema)}"]').click()
            time.sleep(1)
            frame.locator("#form-pesquisa-pessoa\\:btn-selecionar").click()
            time.sleep(2)

            ### Arrumar
            id_input_qualificacao = self.page.query_selector('label:has-text("Qualificação *")').get_attribute('for')
            id_input_qualificacao = id_input_qualificacao.replace(':', '\\:').replace('localizador', 'cnj')
            self.page.query_selector(f"#{id_input_qualificacao}_input").click()
            time.sleep(1)
            self.page.locator(f"#{id_input_qualificacao}_input").type(self.data_input.qualificacao_sistema)
            time.sleep(1)

            id_btn_salvar = f"{id_input_qualificacao.split(':ff-qualificacao')[0]}:btn-salvar-envolvido"
            self.page.locator(f"#{id_btn_salvar}").click()
            time.sleep(5)

            popup = self.page.locator("#modal-litispendencia").is_visible()
            if popup:
                self.page.locator('#modal-litispendencia button:has-text("Fechar")').click()
                time.sleep(5)

        except Exception as error:
             raise Exception("Erro ao inserir dados da autoridade")