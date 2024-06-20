import json
import time
from urllib.parse import urlencode
from playwright.sync_api import Page, BrowserContext, sync_playwright
import requests
from unidecode import unidecode

from modules.logger.Logger import Logger

class BuscarComplementoVaraUseCase:
    def __init__(
        self,
        id_vara: str,
        vara:str,
        complemento_vara: str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.id_vara = id_vara
        self.vara = vara
        self.complemento_vara = complemento_vara
        self.classLogger = classLogger
        self.context = context

    def execute(self)->dict:
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = f"https://booking.nextlegalone.com.br/config/ComplementoVaraTurma/LookupComplementoVaraTurma?parentId={str(self.id_vara)}&term={self.complemento_vara}&pageSize=10&_=1708376406655"

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
                if row.get("Value") == self.complemento_vara:
                    return row

            qtde_varas = json_response.get("Count")

            pages = qtde_varas//10
            if qtde_varas % 10 != 0:
                pages += 1
            
            cont = 1
            while cont < pages:
                url = f"https://booking.nextlegalone.com.br/config/ComplementoVaraTurma/LookupComplementoVaraTurma?parentId={str(self.id_vara)}&term={self.complemento_vara}&pageIndex={str(cont)}&pageSize=10&_=1706729777816"
                headers["Referer"] = url
                response = requests.get(url=url,headers=headers)

                json_response = json.loads(response.text)

                ### Insere os resultados no banco

                for row in json_response.get('Rows'):
                    if row.get("Value") == self.complemento_vara:
                        return row

                time.sleep(0.5)
                cont +=1

            url = f"https://booking.nextlegalone.com.br/config/ComplementoVaraTurma/EditModal"

            body = urlencode({
                "VaraTurmaText":self.vara,
                "VaraTurmaId":self.id_vara,
                "Descricao":self.complemento_vara
            })

            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":url,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str,
                "Content-Type":"application/x-www-form-urlencoded"
            }

            response = requests.post(url=url,data=body,headers=headers)

            json_response = json.loads(response.text)

            if response.status_code == 200:
                return json_response 

            raise Exception ("vara não encontrada")
        except Exception as error:
            message = "Erro ao buscar o cadastro do complemento da vara no Legalone"
            self.classLogger.message(message)
            raise error