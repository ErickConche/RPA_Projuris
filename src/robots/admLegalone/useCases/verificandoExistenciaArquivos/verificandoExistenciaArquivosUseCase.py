import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page, BrowserContext, sync_playwright
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
            message = "Verificando se os arquivos foram salvos."
            self.classLogger.message(message)
            self.page.goto(self.url_pasta)
            time.sleep(10)
            success = False
            attemp = 0
            max_attemp = 3
            while attemp < max_attemp:
                try:
                    self.page.query_selector('#aTab-ecm').click()
                    time.sleep(25)
                    self.page.query_selector('.add-popover-menu.popover-menu-button.main-popover-menu-button.tooltipMenu').hover()
                    time.sleep(10)
                    attemp = max_attemp
                    success = True
                except Exception as error:
                    attemp +=1
                    time.sleep(5)
            if not success:
                message = "Erro ao verificar se os arquivos foram salvos."
                self.classLogger.message(message)
                raise Exception("Erro ao acessar GED")
            
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            trs = site_html.select_one(".search-result-bar-compact").select_one("tbody").select("tr")
            list_files_legalone = []
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