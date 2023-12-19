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
            url_file_main = self.arquivo_principal
            name_file_main = DownloadS3(url=url_file_main).execute()
            UploadArquivoUseCase(
                page=self.page,
                nome_arquivo=name_file_main,
                classLogger=self.classLogger,
                file_main=True,
                list_files=[]
            ).execute()
            if self.arquivos_secundarios != "" and self.arquivos_secundarios != None:
                self.page.goto(self.url_pasta)
                url_file_secundary = self.arquivos_secundarios
                name_file_secundary = DownloadS3(url=url_file_secundary).execute()
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

        except Exception as error:
            raise Exception("Erro ao realizar o upload dos arquivos")