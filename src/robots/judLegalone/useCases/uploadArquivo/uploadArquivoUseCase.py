import os
import time
from typing import List
import global_variables.error_ged_legalone as error_ged_legalone
from playwright.sync_api import Page, BrowserContext, sync_playwright
from modules.logger.Logger import Logger
from robots.judLegalone.useCases.acessarPaginaUpload.acessarPaginaUploadUseCase import AcessarPaginaUploadUseCase

class UploadArquivoUseCase:
    def __init__(
        self,
        page: Page,
        nome_arquivo:str,
        classLogger: Logger,
        list_files: List[str],
        url_pasta: str,
        processo: str,
        file_main: bool = True
    ) -> None:
        self.page = page
        self.nome_arquivo = nome_arquivo
        self.file_main = file_main
        self.classLogger = classLogger
        self.list_files = list_files
        self.url_pasta = url_pasta
        self.processo = processo

    def execute(self):
        try:
            AcessarPaginaUploadUseCase(
                page=self.page,
                classLogger=self.classLogger
            ).execute()
            if len(self.list_files)<=0:
                with self.page.expect_file_chooser() as fc_info:
                    self.page.locator('input[title="file input"]').click()
                file_chooser = fc_info.value
                file_chooser.set_files(self.nome_arquivo)
                time.sleep(35)
                if self.file_main:
                    self.page.locator("#TipoText").click()
                    time.sleep(1)
                    self.page.locator("#TipoText").type("Peça Processual / Petição inicial")
                    time.sleep(1)
                    self.page.locator('#lookup_tipo .lookup-button.lookup-filter').click()
                    time.sleep(5)
                    self.page.locator('#subtipo_24').click()
                    time.sleep(5)
                os.remove(self.nome_arquivo)
                self.page.click('button[name="ButtonSave"][value="0"]')
                    
            time.sleep(15)
        except Exception as error:
            message = f"Erro ao fazer o upload do arquivo {'principal' if self.file_main else 'secundario'}. Erro: {str(error)}"
            self.classLogger.message(message)
            error_ged_legalone.update_error_ged_legalone(True)
            raise error