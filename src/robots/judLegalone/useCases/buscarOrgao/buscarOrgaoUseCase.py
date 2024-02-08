import json
import time
from unidecode import unidecode
from playwright.sync_api import Page, BrowserContext, sync_playwright
import requests

from modules.logger.Logger import Logger

class BuscarOrgaoUseCase:
    def __init__(
        self,
        orgao_julgador: str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.orgao_julgador = orgao_julgador
        self.classLogger = classLogger
        self.context = context

    def execute(self)->dict:
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = f"https://booking.nextlegalone.com.br/config/orgaos/LookupOrgao?idsJurisdicao%5B0%5D=null&idCidade=null&tipo=0&term={self.orgao_julgador}&pageSize=10&_=1706726288660"
            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":"https://booking.nextlegalone.com.br/servicos/servicos/create?returnUrl=%2Fservicos%2Fservicos%2Fsearch%3Fajaxnavigation%3Dtrue",
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }

            response = requests.get(url=url,headers=headers)

            json_response:dict = json.loads(response.text)

            ### Insere os resultados no banco

            return json_response.get('Rows')[0]

        except Exception as error:
            message = "Erro ao buscar o cadastro do Orgao no Legalone"
            self.classLogger.message(message)
            raise error