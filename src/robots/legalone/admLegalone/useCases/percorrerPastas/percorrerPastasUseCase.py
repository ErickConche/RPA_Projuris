import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.legalone.__model__.PastaModel import PastaModel


class PercorrerPastasUseCase:
    def __init__(
        self,
        page: Page,
        nome_envolvido:str, 
        numero_reclamacao:str,
        classLogger: Logger,
        site_html
    ) -> None:
        self.page = page
        self.nome_envolvido = nome_envolvido
        self.numero_reclamacao = numero_reclamacao
        self.classLogger = classLogger
        self.site_html = site_html

    def execute(self)->PastaModel:
        try:
            site_html = self.site_html
            tr_values_html = site_html.select_one('.webgrid.grid-view-column-active').select("tr")
            list_urls = []
            for tr in tr_values_html:
                if tr.attrs.get('class')[0] != 'webgrid-header':
                    href = tr.select("td")[2].select_one("a").attrs.get('href')
                    url = f"https://booking.nextlegalone.com.br{href}"
                    list_urls.append(url)

            for url in list_urls:
                self.page.goto(url)
                time.sleep(5)
                site_html = BeautifulSoup(self.page.content(), 'html.parser')
                divs_person_html = site_html.select_one(".legalone-panel-content")
                protocol_find = divs_person_html.select(".field")[3].text
                if len(protocol_find) > 19:
                    possible_protocol_find = protocol_find.split('.')[-1] + '/2024'
                    if possible_protocol_find == self.numero_reclamacao:
                        protocol_find = possible_protocol_find
                if protocol_find == self.numero_reclamacao:
                    div_abstract_html = site_html.select_one(".cardview-responsive.collapse-panel").select(".row")
                    pasta = div_abstract_html[0].select(".span2")[0].select_one(".value.small-value.first").text
                    data_cadastro = div_abstract_html[10].select(".span2")[0].select_one(".value.small-value").text
                    data_cadastro = data_cadastro.replace("\n","")
                    message = f"Pasta encontrada. Pasta = {str(pasta)}\nData do Cadastro = {str(data_cadastro)}"
                    self.classLogger.message(message)
                    data_pasta: PastaModel = PastaModel(
                        found=True,
                        pasta=pasta,
                        data_cadastro=data_cadastro,
                        url_pasta=self.page.url
                    )
                    return data_pasta
            message = "Não existe pasta para o protocolo do envolvido"
            self.classLogger.message(message)
            data_pasta: PastaModel = PastaModel(
                found=False,
                pasta=None,
                data_cadastro=None
            )
            return data_pasta

        except Exception as error:
            raise Exception ("Erro ao percorrer pastas do envolvido")