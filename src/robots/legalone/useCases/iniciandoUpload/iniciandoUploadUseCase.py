import uuid
import requests
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from robots.legalone.useCases.iniciandoUpload.__model__.iniciandoUploadModel import IniciandoUploadModel


class IniciandoUploadUseCase:
    def __init__(
        self,
        classLogger: Logger,
        url_insert_ged: str,
        headers: dict,
        nome_arquivo: str,
        legalone_jud: bool
    ) -> None:
        self.classLogger = classLogger
        self.url_insert_ged = url_insert_ged
        self.headers = headers
        self.nome_arquivo = nome_arquivo
        self.legalone_jud = legalone_jud

    def execute(self)->IniciandoUploadModel:
        try:
            id_pasta = self.url_insert_ged.split("/CreateArquivo/")[1].split("?")[0]
            response = requests.get(url=self.url_insert_ged, headers=self.headers)
            if response.status_code > 302:
                raise Exception("Erro")
            
            site_html = BeautifulSoup(response.text, 'html.parser')

            tipo_vinculo = 'VinculoProcessoText' if self.legalone_jud else 'VinculoServicoText' 

            id_vinculo = site_html.find('input', {'name': 'Vinculos.Index'})['value']
            pasta = site_html.find('input', {'id': f'Vinculos_{id_vinculo}__{tipo_vinculo}'})['value']
            request_verification_token = site_html.find('input', {'name': '__RequestVerificationToken'})['value']

            posicao_do_ultimo_ponto = self.nome_arquivo.rfind('.')
            extensao = self.nome_arquivo[posicao_do_ultimo_ponto + 1:]
            nome_arquivo_server = f"{str(uuid.uuid4())}.{extensao}"

            return IniciandoUploadModel(
                id_pasta=id_pasta,
                id_vinculo=id_vinculo,
                pasta=pasta,
                request_verification_token=request_verification_token,
                nome_arquivo_server=nome_arquivo_server,
                nome_arquivo=self.nome_arquivo
            )
        except Exception as error:
            message = f"Erro ao iniciar Upload."
            self.classLogger.message(message)
            raise error