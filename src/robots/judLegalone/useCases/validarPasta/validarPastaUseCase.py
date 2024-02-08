import json
import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page, BrowserContext, sync_playwright
import requests

from modules.logger.Logger import Logger
from robots.judLegalone.useCases.validarPasta.__model__.PastaModel import PastaModel

class ValidarPastaJudUseCase:
    def __init__(
        self,
        page: Page,
        nome_envolvido:str, 
        processo:str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.page = page
        self.nome_envolvido = nome_envolvido
        self.processo = processo
        self.classLogger = classLogger
        self.context = context

    def execute(self)->PastaModel:
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = f"https://booking.nextlegalone.com.br/shared/global/search?term={self.processo}&limit=3&useRules=true&tipo=1&searchContextsIds=3&searchContextsIds=4&searchContextsIds=5&searchContextsIds=1&searchContextsIds=2&searchContextsIds=9&searchContextsIds=11&searchContextsIds=12&searchContextsIds=13&_=1706719193954"
            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":url,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }
            response = requests.get(url=url,headers=headers)

            json_response:dict = json.loads(response.text)

            if len(json_response.get("Groups"))<=0:
                message = f"Não existe pasta para o CNJ {self.processo}"
                self.classLogger.message(message)
                data_pasta: PastaModel = PastaModel(
                    found=False,
                    pasta=None,
                    url_pasta=None,
                    protocolo=None
                )
                return data_pasta
            
            else: 
                item:dict = json_response.get("Groups")[0].get("Items")[0]
                protocolo = item.get("Description")
                url_pasta = item.get("Url")
                url_pasta = f"https://booking.nextlegalone.com.br{url_pasta}"
                data_pasta: PastaModel = PastaModel(
                    found=True,
                    pasta=f"Pasta nº {protocolo}",
                    url_pasta=url_pasta,
                    protocolo=protocolo
                )
                message = f"{data_pasta.pasta}"
                self.classLogger.message(message)
                return data_pasta
            
        except Exception as error:
            raise Exception("Erro ao validar se a pasta já existe")