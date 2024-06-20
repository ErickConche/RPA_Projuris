import requests
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.__model__.PastaModel import PastaModel
from robots.legalone.admLegalone.useCases.percorrerPastas.percorrerPastasUseCase import PercorrerPastasUseCase


class ValidarPastaUseCase:
    def __init__(
        self,
        page: Page,
        nome_envolvido:str, 
        numero_reclamacao:str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.page = page
        self.nome_envolvido = nome_envolvido
        self.numero_reclamacao = numero_reclamacao
        self.classLogger = classLogger
        self.context = context

    def execute(self)->PastaModel:
        try:
            envolvido_format = self.nome_envolvido.replace(" ","+")
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = "https://booking.nextlegalone.com.br/servicos/servicos/Search?IsSearchExecutedByUser=true"
            url = url + "&ShowAdvancedFilters=False&ShowBarCodeFilters=False&search-filters-ajax-url=%2fservicos%2fservicos%2fSearchFilters%3fViewName%3dSearchFiltersServicos%26SearchAction%3dSearch&StatusSimples%5b0%5d.Id=1&StatusSimples%5b0%5d.Value=Em+andamento&StatusSimples%5b1%5d.Id=4&StatusSimples%5b1%5d.Value=Arquivado&StatusSimples%5b2%5d.Id=3&StatusSimples%5b2%5d.Value=Conclu%c3%addo&StatusSimples%5b3%5d.Id=2&StatusSimples%5b3%5d.Value=Cadastrado+incorretamente&"
            url = url + f"Search={envolvido_format}&SortBy=Pasta&_SortDirection=DESC"
            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":url,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }
            response = requests.get(url=url,headers=headers)
            site_html = BeautifulSoup(response.text, 'html.parser')
            qtde_pastas = site_html.select_one(".legalone-grid-counter").text.split("Pastas de consultivo encontradas: ")[1]
            if int(qtde_pastas)<=0:
                message = "Não existe pasta para o protocolo do envolvido"
                self.classLogger.message(message)
                data_pasta: PastaModel = PastaModel(
                    found=False,
                    pasta=None,
                    data_cadastro=None,
                    url_pasta=None
                )
                return data_pasta
            else:
                return PercorrerPastasUseCase(
                    page=self.page,
                    nome_envolvido=self.nome_envolvido,
                    numero_reclamacao=self.numero_reclamacao,
                    classLogger=self.classLogger,
                    site_html=site_html
                ).execute()
            
        except Exception as error:
            raise Exception("Erro ao validar se a pasta já existe")