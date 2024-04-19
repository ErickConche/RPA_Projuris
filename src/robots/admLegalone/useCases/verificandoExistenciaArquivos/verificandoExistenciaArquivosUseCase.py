import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page, BrowserContext, sync_playwright
import requests
from modules.downloadS3.downloadS3 import DownloadS3

from modules.logger.Logger import Logger
from robots.admLegalone.useCases.descompactarZip.descompactarZipUseCase import DescompactarZipUseCase
from robots.admLegalone.useCases.verificarExistenciaArquivoPrincipal.verificarExistenciaArquivoPrincipalUseCase import VerificarExistenciaArquivoPrincipal
from robots.admLegalone.useCases.verificarExistenciaArquivoSecundario.verificarExistenciaArquivoSecundarioUseCase import VerificarExistenciaArquivoSecundario

class VerificandoExistenciaArquivosUseCase:
    def __init__(
        self,
        page: Page,
        arquivo_principal: str,
        arquivos_secundarios: str,
        context: BrowserContext,
        pasta: str,
        url_pasta:str,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.arquivo_principal = arquivo_principal
        self.arquivos_secundarios = arquivos_secundarios
        self.context = context
        self.pasta = pasta
        self.url_pasta = url_pasta
        self.classLogger = classLogger

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

            id = self.url_pasta.split("/details/")[1].split("?")[0]

            url = f"https://booking.nextlegalone.com.br/servicos/servicos/detailsged/{str(id)}?renderOnlySection=True&ajaxnavigation=true"

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
                page=self.page,
                arquivo_principal=self.arquivo_principal,
                context=self.context,
                classLogger=self.classLogger,
                list_files_legalone=list_files_legalone
            ).execute()

            name_file_secundary_download = VerificarExistenciaArquivoSecundario(
                page=self.page,
                arquivos_secundarios=self.arquivos_secundarios,
                context=self.context,
                classLogger=self.classLogger,
                list_files_legalone=list_files_legalone
            ).execute()

            return {
                "file_main":name_file_main_download,
                "files_secundary":name_file_secundary_download
            }

        except Exception as error:
            message = "Erro ao verificar se os arquivos foram salvos."
            self.classLogger.message(message)
            raise error