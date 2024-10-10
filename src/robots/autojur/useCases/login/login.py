import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.autojur.useCases.codigoMFA.codigoMfa import codigoMfa


class LoginAutojurUseCase:
    def __init__(
        self,
        page: Page,
        username: str,
        password: str,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.username = username
        self.password = password
        self.classLogger = classLogger
        self.codigoMfa = codigoMfa(username, classLogger)

    def execute(self):
        try:
            self.page.query_selector("#login-form-novo\\:username").click()
            time.sleep(1)
            self.page.query_selector("#login-form-novo\\:username").type(self.username)
            time.sleep(1)
            self.page.query_selector("#login-form-novo\\:password").click()
            time.sleep(1)
            self.page.query_selector("#login-form-novo\\:password").type(self.password)
            time.sleep(1)
            self.page.query_selector("#login-form-novo\\:btn-login").click()
            time.sleep(5)
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            if site_html.select("#form-derrubar-usuario") and self.page.query_selector("#form-derrubar-usuario\\:j_idt74").is_visible():
                self.page.query_selector("#form-derrubar-usuario\\:j_idt74").click()
                time.sleep(5)
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            if site_html.select_one('[id="form-dupla-autenticacao:ff-token"]>div>input') and site_html.select_one('[id="form-dupla-autenticacao:ff-token"]>label').text == 'Chave de Acesso *':
                self.classLogger.message("Aguardando 45 segundos para o envio do código no email")
                time.sleep(45)
                self.classLogger.message("Buscando o código de autenticação no email")
                mfa_code = self.codigoMfa.execute()
                if not mfa_code:
                    raise ("Erro ao coletar o códiga mfa do email")
                self.page.query_selector('[id="form-dupla-autenticacao:ff-token"]>div>input').type(mfa_code)
                self.page.query_selector('[id="form-dupla-autenticacao"]>div>a>i').click()
            if self.page.query_selector('[class="iziToast-message slideIn"]'):
                raise Exception("Erro ao validar o código mfa")
            time.sleep(10)
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            if site_html.select("#user-header"):
                message = "Login finalizado"
                self.classLogger.message(message)
                return
            raise Exception("Erro ao realizar o login")
        except Exception as error:
            raise Exception("Erro ao realizar o login")
