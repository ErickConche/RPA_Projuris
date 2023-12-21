import time
from playwright.sync_api import Page, BrowserContext, sync_playwright
from modules.downloadS3.downloadS3 import DownloadS3

from modules.logger.Logger import Logger
from robots.admLegalone.useCases.descompactarZip.descompactarZipUseCase import DescompactarZipUseCase
from robots.admLegalone.useCases.uploadArquivo.uploadArquivoUseCase import UploadArquivoUseCase

class InserirArquivosUseCase:
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
            message = "Salvando arquivo principal"
            self.classLogger.message(message)
            url_file_main = self.arquivo_principal
            name_file_main = DownloadS3(url=url_file_main).execute()
            UploadArquivoUseCase(
                page=self.page,
                nome_arquivo=name_file_main,
                classLogger=self.classLogger,
                file_main=True,
                list_files=[]
            ).execute()
            message = "Arquivo principal salvo"
            self.classLogger.message(message)
            if self.arquivos_secundarios != "" and self.arquivos_secundarios != "Nenhum arquivo anexado" and self.arquivos_secundarios != None:
                message = "Salvando arquivos secundarios"
                self.classLogger.message(message)
                self.page.goto(self.url_pasta)
                url_file_secundary = self.arquivos_secundarios
                download_success = False
                try:
                    name_file_secundary = DownloadS3(url=url_file_secundary).execute()
                    download_success = True
                except Exception as error:
                    message = "Erro ao fazer o download do arquivo secundario, porém o fluxo não foi interrompido."
                    self.classLogger.message(message)
                if download_success:
                    if '.zip' in name_file_secundary:
                        list_files = DescompactarZipUseCase(
                            name_file_zip=name_file_secundary,
                            classLogger=self.classLogger
                        ).execute()
                        UploadArquivoUseCase(
                            page=self.page,
                            nome_arquivo=name_file_secundary,
                            classLogger=self.classLogger,
                            file_main=False,
                            list_files=list_files
                        ).execute()
                    else:
                        UploadArquivoUseCase(
                            page=self.page,
                            nome_arquivo=name_file_secundary,
                            classLogger=self.classLogger,
                            file_main=False,
                            list_files=[]
                        ).execute()
                    message = "Arquivos secundarios salvos"
                    self.classLogger.message(message)

        except Exception as error:
            raise Exception("Erro ao realizar o upload dos arquivos")