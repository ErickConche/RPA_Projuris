import json
import requests
from unidecode import unidecode
from modules.logger.Logger import Logger
from playwright.sync_api import BrowserContext


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
            url = f"https://booking.nextlegalone.com.br/config/UF/LookupGridUF?filterByDefaultCountry=True&term={self.uf}&pageSize=10&_=1706726796188"
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
                if unidecode(row.get("UFSigla")) == unidecode(self.uf.strip()) \
                or unidecode(row.get("UFText")) == unidecode(self.uf.strip()):
                    return row

            raise Exception ("UF não encontrada")
        except Exception as error:
            message = "Erro ao buscar o cadastro da UF no Legalone"
            self.classLogger.message(message)
            raise error