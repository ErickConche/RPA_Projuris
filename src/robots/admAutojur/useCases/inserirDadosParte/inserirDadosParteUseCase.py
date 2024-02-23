import time
from unidecode import unidecode
from bs4 import BeautifulSoup
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class InserirDadosParteUseCase:
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
            self.page.locator("#painel-envolvidos\\:form-principais-envolvidos\\:j_idt418\\:btn-adicionar-pessoa-vazio").click()
            time.sleep(8)
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            url_iframe = f"https://baz.autojur.com.br{site_html.select_one('iframe').attrs.get('src')}"
            frame = self.page.frame(url=url_iframe)

            frame.fill('#form-pesquisa-pessoa\\:componente-pesquisa-pessoa\\:txt-conteudo',self.data_input.nome_envolvido)
            time.sleep(3)
            frame.locator('button[data-id="form-pesquisa-pessoa:cmbCategoriaPessoa"]').click()
            time.sleep(5)
            frame.locator('li:has-text("Todos")').click()
            time.sleep(5)
            frame.locator("#form-pesquisa-pessoa\\:componente-pesquisa-pessoa\\:btn-pesquisar").click()
            time.sleep(10)
            frame.locator("#form-pesquisa-pessoa\\:ativo").click()
            time.sleep(1)

            site_html = BeautifulSoup(frame.content(), 'html.parser')

            trs = site_html.select_one("#form-pesquisa-pessoa\\:tabela_data").select("tr")
            codigo = None
            time.sleep(5)
            if trs[0].text == 'Nenhum registro encontrado':
                frame.locator("#form-pesquisa-pessoa\\:j_idt92").click()
                time.sleep(5)
                site_html = BeautifulSoup(self.page.content(), 'html.parser')
                url_iframe = f"https://baz.autojur.com.br{site_html.select('iframe')[1].attrs.get('src')}"
                frame = self.page.frame(url=url_iframe)
                frame.locator("#form-tipo-pessoa\\:ff-nome\\:nome").click()
                time.sleep(5)
                frame.locator("#form-tipo-pessoa\\:ff-nome\\:nome").type(self.data_input.nome_envolvido)
                time.sleep(5)
                if frame.locator("#modal-duplicados").is_visible():
                    frame.locator("#modal-duplicados .ui-commandlink.ui-widget.btn.btn-default").click()
                    time.sleep(3)
                frame.fill('#form-tipo-pessoa\\:ff-cpf-cnpj\\:j_idt29',self.data_input.cpf_cnpj_envolvido)
                time.sleep(3)
                if frame.locator("#modal-duplicados").is_visible():
                    frame.locator("#modal-duplicados .ui-commandlink.ui-widget.btn.btn-default").click()
                    time.sleep(3)
                frame.locator("#form-salvar-pessoa\\:j_idt641").click()
                time.sleep(5)
            else:
                for tr in trs:
                    tds = tr.select("td")
                    if unidecode(tds[3].previous.upper()) == unidecode(self.data_input.nome_envolvido.upper()) and \
                       tds[7].text == self.data_input.cpf_cnpj_envolvido:
                        codigo = tds[1].text
                        break
                if not codigo:
                    frame.locator("#form-pesquisa-pessoa\\:j_idt92").click()
                    time.sleep(3)
                    site_html = BeautifulSoup(self.page.content(), 'html.parser')
                    url_iframe = f"https://baz.autojur.com.br{site_html.select('iframe')[1].attrs.get('src')}"
                    frame = self.page.frame(url=url_iframe)
                    frame.locator("#form-tipo-pessoa\\:ff-nome\\:nome").click()
                    time.sleep(1)
                    frame.locator("#form-tipo-pessoa\\:ff-nome\\:nome").type(self.data_input.nome_envolvido)
                    time.sleep(5)
                    if frame.locator("#modal-duplicados").is_visible():
                        frame.locator("#modal-duplicados .ui-commandlink.ui-widget.btn.btn-default").click()
                        time.sleep(3)
                    frame.fill('#form-tipo-pessoa\\:ff-cpf-cnpj\\:j_idt29',self.data_input.cpf_cnpj_envolvido)
                    time.sleep(5)
                    if frame.locator("#modal-duplicados").is_visible():
                        frame.locator("#modal-duplicados .ui-commandlink.ui-widget.btn.btn-default").click()
                        time.sleep(5)
                    frame.locator("#form-salvar-pessoa\\:j_idt641").click()
                    time.sleep(5)
                else:
                    frame.locator(f'tr[data-rk="{codigo}"]').click()
                    time.sleep(1)
                    frame.locator("#form-pesquisa-pessoa\\:btn-selecionar").click()
                    time.sleep(5)
            

            self.page.locator("#j_idt1248\\:form-envolvidos\\:ff-qualificacao\\:autocomplete_input").click()
            time.sleep(1)
            self.page.locator("#j_idt1248\\:form-envolvidos\\:ff-qualificacao\\:autocomplete_input").type(self.data_input.qualificacao_envolvido)
            time.sleep(1)

            self.page.locator("#j_idt1248\\:form-envolvidos\\:btn-salvar-envolvido").click()
            time.sleep(10)

            popup = self.page.locator("#modal-litispendencia").is_visible()
            if popup:
                self.page.locator('#modal-litispendencia button:has-text("Fechar")').click()
                time.sleep(5)
                
        except Exception as error:
            raise Exception("Erro ao inserir dados da parte")