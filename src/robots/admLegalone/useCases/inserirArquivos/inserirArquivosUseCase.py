import time
from playwright.sync_api import Page, BrowserContext, sync_playwright
from modules.downloadS3.downloadS3 import DownloadS3

from modules.logger.Logger import Logger
from robots.admLegalone.useCases.descompactarZip.descompactarZipUseCase import DescompactarZipUseCase
from robots.admLegalone.useCases.uploadArquivo.uploadArquivoUseCase import UploadArquivoUseCase
from robots.admLegalone.useCases.verificandoExistenciaArquivos.verificandoExistenciaArquivosUseCase import VerificandoExistenciaArquivosUseCase

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
            checked_files = VerificandoExistenciaArquivosUseCase(
                page=self.page,
                arquivo_principal=self.arquivo_principal,
                arquivos_secundarios=self.arquivos_secundarios,
                context=self.context,
                pasta=self.pasta,
                url_pasta=self.url_pasta,
                classLogger=self.classLogger
            ).execute()
            if checked_files.get("file_main"):
                UploadArquivoUseCase(
                    page=self.page,
                    nome_arquivo=checked_files.get("file_main"),
                    classLogger=self.classLogger,
                    file_main=True,
                    list_files=[],
                    url_pasta=self.url_pasta
                ).execute()

            if checked_files.get("files_secundary"):
                UploadArquivoUseCase(
                    page=self.page,
                    nome_arquivo=None,
                    classLogger=self.classLogger,
                    file_main=False,
                    list_files=checked_files.get("files_secundary"),
                    url_pasta=self.url_pasta
                ).execute()

        except Exception as error:
            raise Exception("Erro ao realizar o upload dos arquivos")