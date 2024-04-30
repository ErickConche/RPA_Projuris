import time
import requests
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext, sync_playwright


class AcessarPaginaUploadUseCase:
    def __init__(
        self,
        classLogger: Logger,
        context: BrowserContext,
        url_pasta: str
    ) -> None:
        self.classLogger = classLogger
        self.url_pasta = url_pasta
        self.context = context

    def execute(self):
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'

            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":self.url_pasta,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }

            id = self.url_pasta.split("/Details/")[1]

            url = f"https://booking.nextlegalone.com.br/processos/Processos/detailsged/{id}?renderOnlySection=True&ajaxnavigation=true"
            
            response = requests.get(url=url,headers=headers)

            site_html = BeautifulSoup(response.text, 'html.parser')
            lis = site_html.select_one("#popovermenus").select("li")
            url = ""
            for li in lis:
                if li.select_one("a").text == 'Anexar arquivo':
                    href = li.select_one("a").attrs.get('href')
                    url = f"https://booking.nextlegalone.com.br{href}"
                    break
            return url
        except Exception as error:
            message = f"Erro ao acessar a pagina de uploads"
            self.classLogger.message(message)
            raise error