import time
from playwright.sync_api import Page
from modules.logger.Logger import Logger


class LogoutUseCase:
    def __init__(
        self,
        page: Page,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.classLogger = classLogger

    def execute(self):
        try:
            message = "Deslogando do Legalone"
            self.classLogger.message(message)
            self.page.query_selector('[data-title="User Info"]').click()
            time.sleep(1)
            self.page.query_selector('[href="/ca/authentication/logout"]').click()
            time.sleep(5)
            message = "A aplicação deslogou do Legalone"
            self.classLogger.message(message)
        except Exception as error:
            pass