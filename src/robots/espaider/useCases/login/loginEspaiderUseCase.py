from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from playwright.sync_api import Page
import time


class LoginEspaiderUseCase:
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

    def execute(self):
        try:
            return self.login_attempts()
        except Exception as error:
            message = error.args[0]
            self.classLogger.message(message)
            raise Exception("Erro ao realizar o login")

    def login_attempts(self):
        response = {
            "success": True
        }
        max_retries = 5
        attempt = 1
        while max_retries >= attempt:
            self.classLogger.message(f"Tentativa de login [Espaider-Civil] - [Tentativa: {attempt}]")
            self.login_attempt(response=response)
            if not response.get('success'):
                self.classLogger.message(f"Tentativa de login [Espaider-Civil] - [Tentativa: {attempt}]: Falhou")
                attempt += 1
                continue
            return response

    def login_attempt(self, response):
        try:
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            if not site_html.select('#ctUserInfo'):
                self.page.wait_for_load_state('load')
                self.page.fill('#userFieldEdt', self.username)
                self.page.fill('#passwordFieldEdt', self.password)
                self.page.locator('#loginButton').click()
                self.page.wait_for_selector('#ctUserInfo', timeout=10000)
                if not self.page.query_selector('#ctUserInfo'):
                    raise Exception('Credencial incorreta')
            message = '[Espaider-Civil]: Login realizado com succeso'
            self.classLogger.message(message)
            response.update({
                "success": True,
                "message": message
            })
            return response
        except Exception as error:
            print(error)
            response['success'] = False
            return response