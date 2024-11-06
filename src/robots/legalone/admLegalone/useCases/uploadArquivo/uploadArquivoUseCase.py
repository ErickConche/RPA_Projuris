import os
import time
from typing import List
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.useCases.iniciandoUpload.iniciandoUploadUseCase import IniciandoUploadUseCase
from robots.legalone.useCases.uploadArquivoApi.uploadArquivoApiUseCase import UploadArquivoApiUseCase
from robots.legalone.admLegalone.useCases.concluirUploadArquivo.concluirUploadArquivoUseCase import ConcluirUploadArquivoUseCase


class UploadArquivoUseCase:
    def __init__(
        self,
        page: Page,
        nome_arquivo:str,
        classLogger: Logger,
        list_files: List[str],
        url_insert_ged: str,
        context: BrowserContext,
        file_main: bool = True
    ) -> None:
        self.page = page
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
                    headers=headers,
                    legalone_jud=False
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
                            data_inicial_upload = IniciandoUploadUseCase(
                                classLogger=self.classLogger,
                                url_insert_ged=self.url_insert_ged,
                                headers=headers,
                                nome_arquivo=file,
                                legalone_jud=False
                            ).execute()

                            UploadArquivoApiUseCase(
                                classLogger=self.classLogger,
                                data_inicial_upload=data_inicial_upload,
                                headers=headers
                            ).execute()

                            if 'CIP' in file.upper() or 'reclamacao' in file.lower() or 'reclamação' in file.lower():
                                self.file_main=True

                            ConcluirUploadArquivoUseCase(
                                classLogger=self.classLogger,
                                data_inicial_upload=data_inicial_upload,
                                headers=headers,
                                url_insert_ged=self.url_insert_ged,
                                arquivo_principal=self.file_main
                            ).execute()
                            attemp = max_attemp
                            self.file_main=False

                            os.remove(data_inicial_upload.nome_arquivo)
                        except Exception as error:
                            attemp +=1
                            error_function = error
                        time.sleep(1)
                
                if not success and error_function:
                    raise error_function
        except Exception as error:
            message = f"Erro ao fazer o upload do arquivo {'principal' if self.file_main else 'secundario'}. Erro: {str(error)}"
            self.classLogger.message(message)
            raise error
        