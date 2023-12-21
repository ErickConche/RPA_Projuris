import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger

class LoginAdmLegaloneUseCase:
    def __init__(
        self,
        page: Page,
        username:str, 
        password:str,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.username = username
        self.password = password
        self.classLogger = classLogger

    def execute(self):
        try:
            message  = "Iniciando login"
            self.classLogger.message(message)
            self.page.query_selector('#Username').click()
            time.sleep(1)
            self.page.query_selector('#Username').type(self.username)
            time.sleep(1)
            self.page.query_selector('#Password').click()
            time.sleep(1)
            self.page.query_selector('#Password').type(self.password)
            time.sleep(1)
            self.page.query_selector('#SignIn').click()
            time.sleep(15)
            if self.page.query_selector('#menuservicos'):
                print("Login finalizado")
                return
            raise Exception("Erro ao fazer o login")
        except Exception as error:
            raise Exception("Erro ao realizar o login")