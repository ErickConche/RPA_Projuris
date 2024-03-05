import json
import time
from playwright.sync_api import Page, BrowserContext, sync_playwright
import requests
from unidecode import unidecode

from modules.logger.Logger import Logger

class BuscarComarcaUseCase:
    def __init__(
        self,
        comarca: str,
        classLogger: Logger,
        id_uf: int,
        id_justica: int,
        context: BrowserContext
    ) -> None:
        self.id_uf = id_uf
        self.id_justica = id_justica
        self.comarca = comarca
        self.classLogger = classLogger
        self.context = context

    def execute(self)->dict:
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = f"https://booking.nextlegalone.com.br/config/Foro/LookupForo?idUF={str(self.id_uf)}&idJustica={str(self.id_justica)}&term={self.comarca}&pageSize=10&_=1706733430269"

            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":url,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }

            response = requests.get(url=url,headers=headers)

            json_response = json.loads(response.text)

            ### Insere os resultados no banco

            for row in json_response.get('Rows'):
                if row.get("Value") == self.comarca:
                    return row

            qtde_comarcas = json_response.get("Count")

            pages = qtde_comarcas//10
            if qtde_comarcas % 10 != 0:
                pages += 1
            
            cont = 1
            while cont < pages:
                url = f"https://booking.nextlegalone.com.br/config/Foro/LookupForo?idUF={str(self.id_uf)}&pageIndex={str(cont)}&idJustica={str(self.id_justica)}&term={self.comarca}&pageSize=10&_=1706733430269"
                headers["Referer"] = url
                response = requests.get(url=url,headers=headers)

                json_response = json.loads(response.text)

                ### Insere os resultados no banco

                for row in json_response.get('Rows'):
                    if row.get("Value") == self.comarca:
                        return row

                time.sleep(0.5)
                cont +=1

            raise Exception ("comarca não encontrada")
        except Exception as error:
            message = "Erro ao buscar o cadastro da comarca no Legalone"
            self.classLogger.message(message)
            raise error