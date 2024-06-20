import requests
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from playwright.sync_api import BrowserContext


class AcessarPaginaUploadUseCase:
    def __init__(
        self,
        classLogger: Logger,
        context: BrowserContext,
        url_pasta: str,
        legalone_jud: bool
    ) -> None:
        self.classLogger = classLogger
        self.url_pasta = url_pasta
        self.context = context
        self.legalone_jud = legalone_jud

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

            id = self.url_pasta.split("/Details/")[1] if self.legalone_jud else self.url_pasta.split("/details/")[1].split("?")[0]
            path_url = "processos/Processos/" if self.legalone_jud else 'servicos/servicos/'

            url = f"https://booking.nextlegalone.com.br/{path_url}detailsged/{id}?renderOnlySection=True&ajaxnavigation=true"
            
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