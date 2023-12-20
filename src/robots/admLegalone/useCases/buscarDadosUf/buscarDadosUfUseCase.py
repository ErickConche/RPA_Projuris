import json
import time
from unidecode import unidecode
from playwright.sync_api import Page, BrowserContext, sync_playwright
import requests

from modules.logger.Logger import Logger

class BuscarDadosUfUseCase:
    def __init__(
        self,
        uf: str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.uf = uf
        self.classLogger = classLogger
        self.context = context

    def execute(self)->dict:
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = "https://booking.nextlegalone.com.br/config/UF/LookupGridUF?returnUFBrasilAsDefault=False&idPais=&pageSize=28&_=1702581879803"
            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":"https://booking.nextlegalone.com.br/servicos/servicos/create?returnUrl=%2Fservicos%2Fservicos%2Fsearch%3Fajaxnavigation%3Dtrue",
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }

            response = requests.get(url=url,headers=headers)

            json_response = json.loads(response.text)

            ### Insere os resultados no banco

            for row in json_response.get('Rows'):
                if unidecode(row.get("Value")) == unidecode(self.uf):
                    return row

            raise Exception ("UF não encontrada")
        except Exception as error:
            message = "Erro ao buscar o cadastro da UF no Legalone"
            self.classLogger.message(message)
            raise error