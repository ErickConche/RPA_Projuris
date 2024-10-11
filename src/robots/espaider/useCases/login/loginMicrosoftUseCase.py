from bs4 import BeautifulSoup
from playwright.sync_api import Page
from modules.logger.Logger import Logger
import time

class LoginMicrosoftUseCase:
    def __init__(self, user: str, password: str, classLogger: Logger, page: Page) -> None:
        self.user=user
        self.password=password
        self.classLogger=classLogger
        self.page=page

    def execute(self):
        response = {
            "success": True
        }
        try:
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            if not site_html.select('#userOptionsBtn'):
                self.page.wait_for_selector("[name=loginfmt]")
                self.page.query_selector("[name=loginfmt]").type(f'{self.user}@vale.com')
                self.page.query_selector("#idSIButton9").click()
                time.sleep(3)
                self.page.wait_for_selector("passwd")
                self.page.query_selector("passwd").type(self.password)
                self.page.query_selector("#idSIButton9").click()
                time.sleep(5)
            if site_html.select('#userOptionsBtn'):
                self.classLogger("Logado com sucesso")
                return response.update({
                    "success": True,
                    "message": "Logado com sucesso"
                })
        except Exception as e:
            raise Exception("Erro ao relizar login!")
