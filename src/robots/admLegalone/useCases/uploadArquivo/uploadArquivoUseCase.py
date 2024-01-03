import os
import time
from typing import List
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
        file_main: bool = True
    ) -> None:
        self.page = page
        self.nome_arquivo = nome_arquivo
        self.file_main = file_main
        self.classLogger = classLogger
        self.list_files = list_files

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
                time.sleep(60)
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
                files_updated = 0
                for file in self.list_files:
                    with self.page.expect_file_chooser() as fc_info:
                        self.page.locator('input[title="file input"]').click()
                    file_chooser = fc_info.value
                    file_chooser.set_files(file)
                    time.sleep(60)
                    os.remove(file)
                    files_updated += 1
                    if files_updated == 5:
                        self.page.click('button[name="ButtonSave"][value="0"]')
                        time.sleep(15)
                        AcessarPaginaUploadUseCase(
                            page=self.page,
                            classLogger=self.classLogger
                        ).execute()
                        files_updated = 0

                if files_updated != 0:
                    self.page.click('button[name="ButtonSave"][value="0"]')
            time.sleep(15)
        except Exception as error:
            message = f"Erro ao fazer o upload do arquivo {'principal' if self.file_main else 'secundario'}"
            self.classLogger.message(message)
            raise error