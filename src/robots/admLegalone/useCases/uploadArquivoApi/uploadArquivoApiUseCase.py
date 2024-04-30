import requests
from modules.logger.Logger import Logger
from robots.admLegalone.useCases.iniciandoUpload.__model__.iniciandoUploadModel import IniciandoUploadModel


class UploadArquivoApiUseCase:
    def __init__(
        self,
        classLogger: Logger,
        data_inicial_upload: IniciandoUploadModel,
        headers: dict
    ) -> None:
        self.classLogger = classLogger
        self.data_inicial_upload = data_inicial_upload
        self.headers = headers

    def execute(self):
        try:
            url_storage = f"https://booking.nextlegalone.com.br/shared/Azure/GetStorageSas?bloburi=%2Fserver%2Fupload%2F{self.data_inicial_upload.nome_arquivo_server}&_method=PUT&qqtimestamp=1714057716994"
            response_storage = requests.get(url=url_storage, headers=self.headers)
            url_corp = response_storage.text
            headers_corp = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'pt-BR,pt;q=0.9',
                'Access-Control-Request-Headers': 'content-type,x-ms-blob-type,x-ms-meta-qqfilename',
                'Access-Control-Request-Method': 'PUT',
                'Connection': 'keep-alive',
                'Host': 'corpbrprodstorage.blob.core.windows.net',
                'Origin': 'https://booking.nextlegalone.com.br',
                'Referer': 'https://booking.nextlegalone.com.br/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.options(url=url_corp, headers=headers_corp)
            if response.status_code > 302:
                raise Exception("Erro")
            
            headers_corp["X-Ms-Blob-Type"] = 'BlockBlob'
            headers_corp["X-Ms-Meta-Qqfilename"] = self.data_inicial_upload.nome_arquivo
            headers_corp["Content-Length"] = '4890'
            headers_corp["Content-Type"] = 'application/pdf'

            del headers_corp["Access-Control-Request-Headers"]
            del headers_corp["Access-Control-Request-Method"]

            with open(self.data_inicial_upload.nome_arquivo, 'rb') as arquivo:
                response = requests.put(url=url_corp, files={'file': arquivo}, headers=headers_corp)
                if response.status_code > 302:
                    raise Exception("Erro")

            return

        except Exception as error:
            message = f"Erro ao realizar upload do arquivo na nova funcao"
            self.classLogger.message(message)
            raise error