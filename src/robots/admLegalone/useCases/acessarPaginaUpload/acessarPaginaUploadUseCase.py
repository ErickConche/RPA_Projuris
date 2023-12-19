import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger

class AcessarPaginaUploadUseCase:
    def __init__(
        self,
        page: Page,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.classLogger = classLogger

    def execute(self):
        try:
            self.page.query_selector('#aTab-ecm').click()
            time.sleep(10)
            self.page.query_selector('.add-popover-menu.popover-menu-button.main-popover-menu-button.tooltipMenu').hover()
            time.sleep(10)
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            lis = site_html.select_one("#popovermenus").select("li")
            url = ""
            for li in lis:
                if li.select_one("a").text == 'Anexar arquivo':
                    href = li.select_one("a").attrs.get('href')
                    url = f"https://booking.nextlegalone.com.br{href}"
                    break
            self.page.goto(url)
            time.sleep(15)
        except Exception as error:
            message = f"Erro ao acessar a pagina de uploads"
            self.classLogger.message(message)
            raise error