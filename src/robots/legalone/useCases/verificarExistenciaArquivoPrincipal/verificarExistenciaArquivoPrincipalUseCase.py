import time
from typing import List
from bs4 import BeautifulSoup
from playwright.sync_api import Page, BrowserContext, sync_playwright
from modules.downloadS3.downloadS3 import DownloadS3

from modules.logger.Logger import Logger

class VerificarExistenciaArquivoPrincipal:
    def __init__(
        self,
        arquivo_principal: str,
        classLogger: Logger,
        list_files_legalone: List[str],
        processo: str = ''
    ) -> None:
        self.arquivo_principal = arquivo_principal
        self.classLogger = classLogger
        self.list_files_legalone = list_files_legalone
        self.processo = processo

    def execute(self):
        try:
            list_files_legalone = self.list_files_legalone
            infos_split = self.arquivo_principal.split("/")
            name_file = infos_split[len(infos_split)-1]
            last_point_position = name_file.rfind('.')
            name_file_main = name_file[:last_point_position]

            file_main_found = False
            name_file_main_download = None
            for files_legalone in list_files_legalone:
                if self.processo != '' and self.processo in files_legalone or name_file_main in files_legalone:
                    file_main_found = True
                    message = "Arquivo principal já existe"
                    self.classLogger.message(message)
                    break

            if not file_main_found:
                name_file_main_download = DownloadS3(url=self.arquivo_principal,complemento_nome=self.processo).execute()
            return name_file_main_download
        except Exception as error:
            message = "Erro ao verificar se o arquivo principal foi salvo"
            self.classLogger.message(message)