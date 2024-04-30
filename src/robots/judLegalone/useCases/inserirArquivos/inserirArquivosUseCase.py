import time
from playwright.sync_api import Page, BrowserContext, sync_playwright
import global_variables.error_ged_legalone as error_ged_legalone
from modules.downloadS3.downloadS3 import DownloadS3

from modules.logger.Logger import Logger
from robots.judLegalone.useCases.acessarPaginaUpload.acessarPaginaUploadUseCase import AcessarPaginaUploadUseCase
from robots.judLegalone.useCases.uploadArquivo.uploadArquivoUseCase import UploadArquivoUseCase
from robots.judLegalone.useCases.verificandoExistenciaArquivos.verificandoExistenciaArquivosUseCase import VerificandoExistenciaArquivosUseCase

class InserirArquivosUseCase:
    def __init__(
        self,
        arquivo_principal: str,
        context: BrowserContext,
        url_pasta:str,
        processo: str,
        classLogger: Logger
    ) -> None:
        self.arquivo_principal = arquivo_principal
        self.context = context
        self.url_pasta = url_pasta
        self.classLogger = classLogger
        self.processo = processo

    def execute(self):
        try:
            checked_files = VerificandoExistenciaArquivosUseCase(
                arquivo_principal=self.arquivo_principal,
                context=self.context,
                url_pasta=self.url_pasta,
                classLogger=self.classLogger,
                processo=self.processo
            ).execute()
            if checked_files.get("file_main"):
                self.url_insert_ged = AcessarPaginaUploadUseCase(
                    classLogger=self.classLogger,
                    url_pasta=self.url_pasta,
                    context=self.context
                ).execute()
                UploadArquivoUseCase(
                    nome_arquivo=checked_files.get("file_main"),
                    classLogger=self.classLogger,
                    file_main=True,
                    list_files=[],
                    url_insert_ged=self.url_insert_ged,
                    context=self.context
                ).execute()
                checked_files = VerificandoExistenciaArquivosUseCase(
                    arquivo_principal=self.arquivo_principal,
                    context=self.context,
                    url_pasta=self.url_pasta,
                    classLogger=self.classLogger,
                    processo=self.processo
                ).execute()
                if checked_files.get("file_main"):
                    raise Exception("Erro")

            error_ged_legalone.update_error_ged_legalone(False)
        except Exception as error:
            raise Exception("Erro ao realizar o upload dos arquivos")