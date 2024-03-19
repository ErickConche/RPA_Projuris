import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger

class LoginJudAutojurUseCase:
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
            self.page.query_selector("#login-form-novo\\:username").click()
            time.sleep(1)
            self.page.query_selector("#login-form-novo\\:username").type(self.username)
            time.sleep(1)
            self.page.query_selector("#login-form-novo\\:password").click()
            time.sleep(1)
            self.page.query_selector("#login-form-novo\\:password").type(self.password)
            time.sleep(1)
            self.page.query_selector("#login-form-novo\\:btn-login").click()
            time.sleep(10)
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            if site_html.select("#form-derrubar-usuario"):
                self.page.query_selector("#form-derrubar-usuario\\:j_idt74").click()
                time.sleep(10)
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            if site_html.select("#user-header"):
                message = "Login finalizado"
                self.classLogger.message(message)
                return
            raise Exception("Erro ao realizar o login")
        except Exception as error:
            raise Exception("Erro ao realizar o login")