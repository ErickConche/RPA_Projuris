import os
import time
from typing import List
import global_variables.error_ged_legalone as error_ged_legalone
from playwright.sync_api import BrowserContext, sync_playwright
from modules.logger.Logger import Logger
from robots.judLegalone.useCases.acessarPaginaUpload.acessarPaginaUploadUseCase import AcessarPaginaUploadUseCase
from robots.judLegalone.useCases.concluirUploadArquivo.concluirUploadArquivoUseCase import ConcluirUploadArquivoUseCase
from robots.judLegalone.useCases.iniciandoUpload.iniciandoUploadUseCase import IniciandoUploadUseCase
from robots.judLegalone.useCases.uploadArquivoApi.uploadArquivoApiUseCase import UploadArquivoApiUseCase

class UploadArquivoUseCase:
    def __init__(
        self,
        nome_arquivo:str,
        classLogger: Logger,
        list_files: List[str],
        url_insert_ged: str,
        context: BrowserContext,
        file_main: bool = True
    ) -> None:
        self.nome_arquivo = nome_arquivo
        self.file_main = file_main
        self.classLogger = classLogger
        self.list_files = list_files
        self.url_insert_ged = url_insert_ged
        self.context = context

    def execute(self):
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'

            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":self.url_insert_ged,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }
            if len(self.list_files)<=0:
                data_inicial_upload = IniciandoUploadUseCase(
                    classLogger=self.classLogger,
                    url_insert_ged=self.url_insert_ged,
                    nome_arquivo=self.nome_arquivo,
                    headers=headers
                ).execute()

                UploadArquivoApiUseCase(
                    classLogger=self.classLogger,
                    data_inicial_upload=data_inicial_upload,
                    headers=headers
                ).execute()

                ConcluirUploadArquivoUseCase(
                    classLogger=self.classLogger,
                    data_inicial_upload=data_inicial_upload,
                    headers=headers,
                    url_insert_ged=self.url_insert_ged,
                    arquivo_principal=True
                ).execute()
                os.remove(data_inicial_upload.nome_arquivo)
        except Exception as error:
            message = f"Erro ao fazer o upload do arquivo {'principal' if self.file_main else 'secundario'}. Erro: {str(error)}"
            self.classLogger.message(message)
            error_ged_legalone.update_error_ged_legalone(True)
            raise error