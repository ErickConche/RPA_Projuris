from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
import global_variables.error_ged_legalone as error_ged_legalone
from robots.legalone.admLegalone.useCases.uploadArquivo.uploadArquivoUseCase import UploadArquivoUseCase
from robots.legalone.useCases.acessarPaginaUpload.acessarPaginaUploadUseCase import AcessarPaginaUploadUseCase
from robots.legalone.admLegalone.useCases.verificandoExistenciaArquivos.verificandoExistenciaArquivosUseCase import VerificandoExistenciaArquivosUseCase


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
        self.url_insert_ged = ''

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

            if checked_files.get("file_main") or checked_files.get("files_secundary"):
                self.url_insert_ged = AcessarPaginaUploadUseCase(
                    classLogger=self.classLogger,
                    url_pasta=self.url_pasta,
                    context=self.context,
                    legalone_jud=False
                ).execute()

                prioritize_files=self.prioritize_files(checked_files)
                
                if prioritize_files:
                    UploadArquivoUseCase(
                        page=self.page,
                        nome_arquivo=prioritize_files[0],
                        classLogger=self.classLogger,
                        file_main=False,
                        list_files=prioritize_files,
                        url_insert_ged=self.url_insert_ged,
                        context=self.context
                    ).execute()

                checked_files = VerificandoExistenciaArquivosUseCase(
                    page=self.page,
                    arquivo_principal=self.arquivo_principal,
                    arquivos_secundarios=self.arquivos_secundarios,
                    context=self.context,
                    pasta=self.pasta,
                    url_pasta=self.url_pasta,
                    classLogger=self.classLogger
                ).execute()
                if checked_files.get("file_main") or checked_files.get("files_secundary"):
                    raise Exception("Erro")
            error_ged_legalone.update_error_ged_legalone(False)
        except Exception as error:
            raise Exception("Erro ao realizar o upload dos arquivos")
        
    def prioritize_files(self, checked_files):
        cip_files = []
        other_files = []
        tnf_files = []

        concat_files = checked_files.get("file_main", []) + checked_files.get("files_secundary", [])

        for file_name in concat_files:
            if 'CIP' in file_name or 'reclamacao' in file_name or 'reclamação' in file_name:
                cip_files.append(file_name)
            elif 'TNF' in file_name: 
                tnf_files.append(file_name)
            else:
                other_files.append(file_name)

        sorted_files = cip_files + other_files + tnf_files
        return sorted_files
