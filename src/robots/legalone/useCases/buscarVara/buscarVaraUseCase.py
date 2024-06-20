import json
import time
import requests
from modules.logger.Logger import Logger
from playwright.sync_api import BrowserContext


class BuscarVaraUseCase:
    def __init__(
        self,
        vara: str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.vara = vara
        self.classLogger = classLogger
        self.context = context

    def execute(self)->dict:
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = f"https://booking.nextlegalone.com.br/config/VaraTurma/LookupVaraTurma?term={self.vara}&pageSize=10&_=1706729777816"

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
                if row.get("Value") == self.vara:
                    return row

            qtde_varas = json_response.get("Count")

            pages = qtde_varas//10
            if qtde_varas % 10 != 0:
                pages += 1
            
            cont = 1
            while cont < pages:
                url = f"https://booking.nextlegalone.com.br/config/VaraTurma/LookupVaraTurma?term={self.vara}&pageIndex={str(cont)}&pageSize=10&_=1706729777816"
                headers["Referer"] = url
                response = requests.get(url=url,headers=headers)

                json_response = json.loads(response.text)

                ### Insere os resultados no banco

                for row in json_response.get('Rows'):
                    if row.get("Value") == self.vara:
                        return row

                time.sleep(0.5)
                cont +=1

            raise Exception ("vara não encontrada")
        except Exception as error:
            message = "Erro ao buscar o cadastro da vara no Legalone"
            self.classLogger.message(message)
            raise error