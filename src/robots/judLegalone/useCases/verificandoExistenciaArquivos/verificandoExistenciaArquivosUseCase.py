import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page, BrowserContext, sync_playwright
from modules.downloadS3.downloadS3 import DownloadS3

from modules.logger.Logger import Logger
from robots.judLegalone.useCases.verificarExistenciaArquivoPrincipal.verificarExistenciaArquivoPrincipalUseCase import VerificarExistenciaArquivoPrincipal

class VerificandoExistenciaArquivosUseCase:
    def __init__(
        self,
        page: Page,
        arquivo_principal: str,
        context: BrowserContext,
        pasta: str,
        url_pasta:str,
        processo:str,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.arquivo_principal = arquivo_principal
        self.context = context
        self.pasta = pasta
        self.url_pasta = url_pasta
        self.classLogger = classLogger
        self.processo = processo

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