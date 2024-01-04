import time
from typing import List
from bs4 import BeautifulSoup
from playwright.sync_api import Page, BrowserContext, sync_playwright
from modules.downloadS3.downloadS3 import DownloadS3

from modules.logger.Logger import Logger
from robots.admLegalone.useCases.descompactarZip.descompactarZipUseCase import DescompactarZipUseCase

class VerificarExistenciaArquivoSecundario:
    def __init__(
        self,
        page: Page,
        arquivos_secundarios: str,
        context: BrowserContext,
        classLogger: Logger,
        list_files_legalone:List[str]
    ) -> None:
        self.page = page
        self.arquivos_secundarios = arquivos_secundarios
        self.context = context
        self.classLogger = classLogger
        self.list_files_legalone = list_files_legalone

    def execute(self):
        try:
            list_files_legalone = self.list_files_legalone
            if self.arquivos_secundarios == "" or self.arquivos_secundarios == "Nenhum arquivo anexado" or self.arquivos_secundarios == None:
                return None
            if '.zip' not in self.arquivos_secundarios:
                infos_split = self.arquivos_secundarios.split("/")
                name_file = infos_split[len(infos_split)-1]
                last_point_position = name_file.rfind('.')
                name_file_secundary= name_file[:last_point_position]
                file_secundary_found = False
                name_file_secundary_download = None
                for files_legalone in list_files_legalone:
                    if name_file_secundary in files_legalone:
                        file_secundary_found = True
                        message = "Arquivo secundario já existe"
                        self.classLogger.message(message)
                        break

                if not file_secundary_found:
                    name_file_secundary_download = [DownloadS3(url=self.arquivos_secundarios).execute()]

                return name_file_secundary_download
            else:
                name_file_secundary = DownloadS3(url=self.arquivos_secundarios).execute()
                list_downloads = DescompactarZipUseCase(
                    name_file_zip=name_file_secundary,
                    classLogger=self.classLogger
                ).execute()
                list_updates = []
                for downloads in list_downloads:
                    file_found = False
                    for files_legalone in list_files_legalone:
                        if downloads.get("nome_original") in files_legalone:
                            file_found = True
                            break
                    if not file_found:
                        list_updates.append(downloads.get("novo_nome_arquivo"))
                if len(list_updates)<=0:
                    list_updates = None
                return list_updates
        except Exception as error:
            message = "Erro ao verificar se o arquivo secundario foi salvo"
            self.classLogger.message(message)