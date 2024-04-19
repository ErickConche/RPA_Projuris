import os
import time
from typing import List
import global_variables.error_ged_legalone as error_ged_legalone
from playwright.sync_api import Page, BrowserContext, sync_playwright
from modules.logger.Logger import Logger
from robots.admLegalone.useCases.acessarPaginaUpload.acessarPaginaUploadUseCase import AcessarPaginaUploadUseCase

class UploadArquivoUseCase:
    def __init__(
        self,
        page: Page,
        nome_arquivo:str,
        classLogger: Logger,
        list_files: List[str],
        url_insert_ged: str,
        file_main: bool = True
    ) -> None:
        self.page = page
        self.nome_arquivo = nome_arquivo
        self.file_main = file_main
        self.classLogger = classLogger
        self.list_files = list_files
        self.url_insert_ged = url_insert_ged

    def execute(self):
        try:
            self.page.goto(self.url_insert_ged)
            time.sleep(5)
            if len(self.list_files)<=0:
                with self.page.expect_file_chooser() as fc_info:
                    self.page.locator('input[title="file input"]').click()
                file_chooser = fc_info.value
                file_chooser.set_files(self.nome_arquivo)
                time.sleep(30)
                if self.file_main:
                    self.page.locator("#TipoText").click()
                    time.sleep(1)
                    self.page.locator("#TipoText").type("Administrativo / Notificação")
                    time.sleep(1)
                    self.page.locator('#lookup_tipo .lookup-button.lookup-filter').click()
                    time.sleep(8)
                    self.page.locator('#subtipo_55').click()
                    time.sleep(5)
                os.remove(self.nome_arquivo)
                self.page.click('button[name="ButtonSave"][value="0"]')
            else:
                error_function = None
                success = False
                for file in self.list_files:
                    attemp = 0 
                    max_attemp = 3
                    while attemp < max_attemp:
                        try:
                            message = f"Iniciando a inserção na caixa de seleção do arquivo secundario {file}"
                            self.classLogger.message(message)
                            with self.page.expect_file_chooser() as fc_info:
                                self.page.locator('input[title="file input"]').click()
                            file_chooser = fc_info.value
                            file_chooser.set_files(file)
                            time.sleep(30)
                            os.remove(file)
                            self.page.click('button[name="ButtonSave"][value="0"]')
                            message = f"Arquivo secundario {file}, inserido na caixa de seleção e persistido"
                            self.classLogger.message(message)
                            time.sleep(3)
                            attemp = max_attemp
                        except Exception as error:
                            attemp +=1
                            error_function = error
                            self.page.goto(self.url_insert_ged)
                            time.sleep(5)
                    self.page.goto(self.url_insert_ged)
                
                if not success and error_function:
                    raise error_function
                    
            time.sleep(5)
        except Exception as error:
            message = f"Erro ao fazer o upload do arquivo {'principal' if self.file_main else 'secundario'}. Erro: {str(error)}"
            self.classLogger.message(message)
            error_ged_legalone.update_error_ged_legalone(True)
            raise error