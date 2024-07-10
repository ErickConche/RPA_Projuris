import time
from unidecode import unidecode
from bs4 import BeautifulSoup
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

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

    def esperar_iframe(self, retry: int = 0):
        if retry > 30:
            message = "Erro ao abrir pagina das partes principais"
            self.classLogger.message(message)
            raise Exception(message)
        site_html = BeautifulSoup(self.page.content(), 'html.parser')
        if site_html.select_one('iframe'):
            return True
        time.sleep(2)
        return self.esperar_iframe(retry + 1)

    def execute(self):
        try:
            self.page.locator("#painel-envolvidos\\:form-principais-envolvidos\\:j_idt418\\:btn-adicionar-pessoa-vazio").click()
            time.sleep(5)
            self.classLogger.message("Aguadaremos 60 segundos até abertura do modal de partes")
            self.esperar_iframe()
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
            time.sleep(7)
            frame.locator("#form-pesquisa-pessoa\\:ativo").click()
            time.sleep(1)

            site_html = BeautifulSoup(frame.content(), 'html.parser')

            trs = site_html.select_one("#form-pesquisa-pessoa\\:tabela_data").select("tr")
            codigo = None
            time.sleep(5)
            if trs[0].text == 'Nenhum registro encontrado':
                self.classLogger.message(f"Não encontrado nenhum envolvido com nome parecido {self.data_input.nome_envolvido}")
                frame.locator("#form-pesquisa-pessoa\\:j_idt91").click()
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
                frame.locator("#form-salvar-pessoa\\:j_idt662").click()
                time.sleep(5)
            else:
                for tr in trs:
                    tds = tr.select("td")
                    if unidecode(tds[3].previous.upper()) == unidecode(self.data_input.nome_envolvido.upper()) and \
                       tds[7].text == self.data_input.cpf_cnpj_envolvido:
                        self.classLogger.message(f"Envolvido encontrado: {self.data_input.nome_envolvido}")
                        codigo = tds[1].text
                        break
                if not codigo:
                    self.classLogger.message(f"Não encontrado o registro da parte {self.data_input.nome_envolvido}")
                    frame.locator("#form-pesquisa-pessoa\\:j_idt91").click()
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
                    frame.locator("#form-salvar-pessoa\\:j_idt662").click()
                    time.sleep(5)
                    self.classLogger.message(f"Inserido envolvido {self.data_input.nome_envolvido}")
                else:
                    frame.locator(f'tr[data-rk="{codigo}"]').click()
                    time.sleep(1)
                    frame.locator("#form-pesquisa-pessoa\\:btn-selecionar").click()
                    time.sleep(5)
            
            self.classLogger.message(f"Vinculando o envolvido {self.data_input.nome_envolvido} a pasta")
            self.page.locator("#j_idt1250\\:form-envolvidos\\:ff-qualificacao\\:autocomplete_input").click()
            time.sleep(1)
            self.page.locator("#j_idt1250\\:form-envolvidos\\:ff-qualificacao\\:autocomplete_input").type(self.data_input.qualificacao_envolvido)
            time.sleep(1)
            self.classLogger.message(f"Inserida a qualificação {self.data_input.qualificacao_envolvido}")

            self.page.locator("#j_idt1250\\:form-envolvidos\\:btn-salvar-envolvido").click()
            time.sleep(5)
            self.classLogger.message(f"Envolvido vinculado a pasta")

            popup = self.page.locator("#modal-litispendencia").is_visible()
            if popup:
                self.page.locator('#modal-litispendencia button:has-text("Fechar")').click()
                time.sleep(5)
                
        except Exception as error:
            raise Exception(f"Erro ao inserir dados da parte, erro: {str(error)}")