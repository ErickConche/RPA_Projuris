import requests
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from playwright.sync_api import BrowserContext
from robots.legalone.useCases.verificarExistenciaArquivoPrincipal.verificarExistenciaArquivoPrincipalUseCase import VerificarExistenciaArquivoPrincipal

class VerificandoExistenciaArquivosUseCase:
    def __init__(
        self,
        arquivo_principal: str,
        context: BrowserContext,
        url_pasta:str,
        processo:str,
        classLogger: Logger
    ) -> None:
        self.arquivo_principal = arquivo_principal
        self.context = context
        self.url_pasta = url_pasta
        self.classLogger = classLogger
        self.processo = processo

    def execute(self):
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'

            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":self.url_pasta,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }

            id = self.url_pasta.split("/Details/")[1]

            url = f"https://booking.nextlegalone.com.br/processos/Processos/detailsged/{id}?renderOnlySection=True&ajaxnavigation=true"

            response = requests.get(url=url,headers=headers)

            message = "Verificando se os arquivos foram salvos."
            self.classLogger.message(message)

            site_html = BeautifulSoup(response.text, 'html.parser')
            
            list_files_legalone = []

            if len(site_html.select_one(".search-result-bar-compact").select("tbody")) > 0:
                trs = site_html.select_one(".search-result-bar-compact").select_one("tbody").select("tr")
                for tr in trs:
                    list_files_legalone.append(tr.select("td")[2].select_one("a").text)
                
            name_file_main_download = VerificarExistenciaArquivoPrincipal(
                arquivo_principal=self.arquivo_principal,
                classLogger=self.classLogger,
                list_files_legalone=list_files_legalone,
                processo=self.processo
            ).execute()

            return {
                "file_main":name_file_main_download
            }

        except Exception as error:
            message = "Erro ao verificar se os arquivos foram salvos."
            self.classLogger.message(message)
            raise error