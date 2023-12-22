import json
import time
from playwright.sync_api import Page, BrowserContext, sync_playwright
import requests
from unidecode import unidecode

from modules.logger.Logger import Logger

class BuscarDadosCidadeUseCase:
    def __init__(
        self,
        id_uf: int,
        cidade: str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.id_uf = id_uf
        self.cidade = cidade
        self.classLogger = classLogger
        self.context = context

    def execute(self)->dict:
        try:
            if self.cidade == 'Barra do Sul':
                self.cidade = 'Balneário Barra do Sul'
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = f"https://booking.nextlegalone.com.br/config/Cidades/LookupCidade?idUF={str(self.id_uf)}&pageSize=50&_=1702583024801"
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
                if row.get("Value") == self.cidade:
                    return row

            qtde_cidades = json_response.get("Count")

            pages = qtde_cidades//50
            if qtde_cidades % 50 != 0:
                pages += 1
            
            cont = 1
            while cont < 50:
                url = f"https://booking.nextlegalone.com.br/config/Cidades/LookupCidade?idUF={str(self.id_uf)}&pageSize=50&pageIndex={str(cont+1)}&_=1702583024801"
                response = requests.get(url=url,headers=headers)

                json_response = json.loads(response.text)

                ### Insere os resultados no banco

                for row in json_response.get('Rows'):
                    if unidecode(row.get("Value")) == unidecode(self.cidade):
                        return row

                time.sleep(0.5)
                cont +=1

            raise Exception ("Cidade não encontrada")
        except Exception as error:
            message = "Erro ao buscar o cadastro da Cidade no Legalone"
            self.classLogger.message(message)
            raise error