import json
import requests
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.__model__.PastaModel import PastaModel


class ValidarPastaJudUseCase:
    def __init__(
        self,
        page: Page,
        nome_envolvido:str, 
        processo:str,
        processo_originario: str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.page = page
        self.nome_envolvido = nome_envolvido
        self.processo = processo
        self.classLogger = classLogger
        self.context = context
        self.processo_originario = processo_originario

    def execute(self)->PastaModel:
        try:
            is_indelizatorio = True if self.processo_originario != '' else False
            processo_buscar = self.processo_originario if is_indelizatorio else self.processo
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = f"https://booking.nextlegalone.com.br/shared/global/search?term={processo_buscar}&limit=3&useRules=true&tipo=1&searchContextsIds=3&searchContextsIds=4&searchContextsIds=5&searchContextsIds=1&searchContextsIds=2&searchContextsIds=9&searchContextsIds=11&searchContextsIds=12&searchContextsIds=13&_=1706719193954"
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
                    protocolo=None,
                    data_cadastro=None,
                    url_pasta_originaria=None
                )
                return data_pasta
            
            else: 
                item:dict = json_response.get("Groups")[0].get("Items")[0]
                url_pasta = item.get("Url")
                url_pasta = f"https://booking.nextlegalone.com.br{url_pasta}"
                response = requests.get(url=url_pasta,headers=headers)
                if not is_indelizatorio:
                    site_html = BeautifulSoup(response.text, 'html.parser')
                    data_cadastro = None
                    rows = site_html.select(".row")
                    for row in rows:
                        if row.find("div", class_="header small-header", text="Data do cadastro"):
                            data_cadastro = row.select("a")[0].text
                            break
                    protocolo = item.get("Description")
                    data_pasta: PastaModel = PastaModel(
                        found=True,
                        pasta=f"Pasta nº {protocolo}",
                        url_pasta=url_pasta,
                        protocolo=protocolo,
                        data_cadastro=data_cadastro,
                        url_pasta_originaria=None
                    )
                    message = f"{data_pasta.pasta}"
                    self.classLogger.message(message)
                    return data_pasta
                
                else: 
                    url_pasta_originaria = url_pasta
                    id_pasta = url_pasta.split("/Details/")[1]
                    url_details_pasta = f"https://booking.nextlegalone.com.br/processos/Processos/DetailsVinculos/{id_pasta}?renderOnlySection=True&ajaxnavigation=true"
                    response = requests.get(url=url_details_pasta,headers=headers)
                    site_html = BeautifulSoup(response.text, 'html.parser')
                    if site_html.select_one(".search-result-bar-compact-no-overflow").select_one("tbody"):
                        trs = site_html.select_one(".search-result-bar-compact-no-overflow").select_one("tbody").select("tr")
                        for tr in trs:
                            tds =tr.select("td")
                            if tds[2].text == 'Incidente':
                                protocolo = tds[1].text
                                url_pasta = tds[1].select_one("a").attrs.get("href")
                                url_pasta = f"https://booking.nextlegalone.com.br{url_pasta}"
                                response = requests.get(url=url_pasta,headers=headers)
                                site_html = BeautifulSoup(response.text, 'html.parser')
                                rows = site_html.select(".row")
                                for row in rows:
                                    if row.find("div", class_="header small-header", text="Número CNJ"):
                                        if row.select(".value.small-value")[1].text != self.processo:
                                            break
                                        elif row.select(".value.small-value")[1].text == self.processo:
                                            data_cadastro = None
                                            for row in rows:
                                                if row.find("div", class_="header small-header", text="Data do cadastro"):
                                                    data_cadastro = row.select("a")[0].text
                                                    break
                                            data_pasta: PastaModel = PastaModel(
                                                found=True,
                                                pasta=f"Pasta nº {protocolo}",
                                                url_pasta=url_pasta,
                                                protocolo=protocolo,
                                                data_cadastro=data_cadastro,
                                                url_pasta_originaria=url_pasta_originaria
                                            )
                                            message = f"{data_pasta.pasta}"
                                            self.classLogger.message(message)
                                            return data_pasta
                    message = f"Não existe pasta para o CNJ {self.processo}"
                    self.classLogger.message(message)
                    data_pasta: PastaModel = PastaModel(
                        found=False,
                        pasta=None,
                        url_pasta=None,
                        protocolo=None,
                        data_cadastro=None,
                        url_pasta_originaria=url_pasta_originaria
                    )
                    return data_pasta
                            
        except Exception as error:
            raise Exception("Erro ao validar se a pasta já existe")