import os
import time
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from modules.downloadS3.downloadS3 import DownloadS3
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirArquivosUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        name_file_main_download = DownloadS3(url=self.data_input.arquivo_principal).execute()
        try:
            self.page.locator('button[data-id="ged-panel-processo:ged-body:form-upload:select-tipo-documento"]').click()
            time.sleep(3)
            self.page.locator('#ged-panel-processo\\:ged-body\\:form-upload .bs-searchbox input').click()
            time.sleep(3)
            self.page.locator('#ged-panel-processo\\:ged-body\\:form-upload .bs-searchbox input').type("NOTIFICAÇÃO")
            time.sleep(3)
            self.page.locator('li:has-text("NOTIFICAÇÃO")').click()
            time.sleep(3)
            file_input = self.page.locator('#ged-panel-processo\\:ged-body\\:form-upload\\:btn-upload_input')
            file_input.set_input_files(name_file_main_download)
            time.sleep(30)
        except Exception as error:
            message = "Erro ao inserir arquivos"
            self.classLogger.message(message)
            raise error
        finally:
            os.remove(name_file_main_download)