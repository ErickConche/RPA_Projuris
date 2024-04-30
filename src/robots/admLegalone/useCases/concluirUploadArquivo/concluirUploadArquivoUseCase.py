import requests
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from robots.admLegalone.useCases.gerarBodyConclusaoUpload.gerarBodyConclusaoUploadUseCase import GerarBodyConclusaoUploadUseCase
from robots.admLegalone.useCases.iniciandoUpload.__model__.iniciandoUploadModel import IniciandoUploadModel


class ConcluirUploadArquivoUseCase:
    def __init__(
        self,
        classLogger: Logger,
        data_inicial_upload: IniciandoUploadModel,
        headers: dict,
        url_insert_ged: str,
        arquivo_principal: bool = True
    ) -> None:
        self.classLogger = classLogger
        self.data_inicial_upload = data_inicial_upload
        self.headers = headers
        self.arquivo_principal = arquivo_principal
        self.url_insert_ged = url_insert_ged

    def execute(self):
        try:
            body = GerarBodyConclusaoUploadUseCase(
                data_inicial_upload=self.data_inicial_upload,
                cookies_str=self.headers['Cookie'],
                arquivo_principal=self.arquivo_principal
            ).execute()
            self.headers["Content-Type"] = "application/x-www-form-urlencoded"

            requests.post(url=self.url_insert_ged, data=body, headers=self.headers)
        except Exception as error:
            message = f"Erro ao realizar upload do arquivo na nova funcao"
            self.classLogger.message(message)
            raise error