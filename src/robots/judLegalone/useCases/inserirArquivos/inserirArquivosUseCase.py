import time
from playwright.sync_api import Page, BrowserContext, sync_playwright
import global_variables.error_ged_legalone as error_ged_legalone
from modules.downloadS3.downloadS3 import DownloadS3

from modules.logger.Logger import Logger
from robots.judLegalone.useCases.uploadArquivo.uploadArquivoUseCase import UploadArquivoUseCase
from robots.judLegalone.useCases.verificandoExistenciaArquivos.verificandoExistenciaArquivosUseCase import VerificandoExistenciaArquivosUseCase

class InserirArquivosUseCase:
    def __init__(
        self,
        page: Page,
        arquivo_principal: str,
        context: BrowserContext,
        pasta: str,
        url_pasta:str,
        processo: str,
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
            checked_files = VerificandoExistenciaArquivosUseCase(
                page=self.page,
                arquivo_principal=self.arquivo_principal,
                context=self.context,
                pasta=self.pasta,
                url_pasta=self.url_pasta,
                classLogger=self.classLogger,
                processo=self.processo
            ).execute()
            if checked_files.get("file_main"):
                UploadArquivoUseCase(
                    page=self.page,
                    nome_arquivo=checked_files.get("file_main"),
                    classLogger=self.classLogger,
                    file_main=True,
                    list_files=[],
                    url_pasta = self.url_pasta,
                    processo=self.processo
                ).execute()

            error_ged_legalone.update_error_ged_legalone(False)
        except Exception as error:
            raise Exception("Erro ao realizar o upload dos arquivos")