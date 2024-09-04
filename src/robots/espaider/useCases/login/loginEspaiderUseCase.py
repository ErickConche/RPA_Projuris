import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page
from modules.logger.Logger import Logger


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
            self.classLogger.message(f"Tentativa de login [Espaider] - [Tentativa: {attempt}]")
            self.login_attempt(response=response)
            if not response.get('success'):
                self.classLogger.message(f"Tentativa de login [Espaider] - [Tentativa: {attempt}]: Falhou")
                attempt += 1
                continue
            return response

    def login_attempt(self, response):
        try:
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            if not site_html.select('#userOptionsBtn'):
                self.page.wait_for_load_state('load')
                self.page.fill('#userFieldEdt', self.username)
                self.page.fill('#passwordFieldEdt', self.password)
                self.page.locator('#loginButton').click()
                self.page.wait_for_load_state('load')
                if self.page.get_by_text("Vídeo de boas vindas").is_visible():
                    self.page.locator("button[data-icon='close']").click()
                self.page.wait_for_load_state('load')
                time.sleep(15)
                if not self.page.query_selector('#userOptionsBtn'):
                    raise Exception('Credencial incorreta')
                if self.page.locator('[data-icon="close"]').is_visible():
                    self.page.query_selector('[data-icon="close"]').click()
                if self.page.locator('tour-popup > tour-popup-actions > button').is_visible():
                    self.page.query_selector('tour-popup > tour-popup-actions > button').click()
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
