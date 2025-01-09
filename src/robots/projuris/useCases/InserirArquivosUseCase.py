import os
import time
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from modules.downloadS3.downloadS3 import DownloadS3

class InserirArquivosProjurisUseCase:
    def __init__(
        self,
        page: Page,
        arquivo_url: str,
        tipo_documento: str,
        data_inclusao_doc:str,
        logger: Logger
    ) -> None:
        """
            Classe para inserir arquivos no Projuris com base em uma URL do S3.
        """
        self.page = page
        self.arquivo_url = arquivo_url
        self.tipo_documento = tipo_documento
        self.data_inclusao_doc = data_inclusao_doc
        self.logger = logger

    def execute(self)-> None:
        """
            Realiza o download do arquivo do S3, seleciona o tipo de documento e faz o upload no Projuris.
        """
        # Baixar o arquivo principal do S3
        name_file_main_download = DownloadS3(url=self.arquivo_url).execute()

        try:
            # Selecionar o tipo de documento
            self.page.locator('button[data-id="projuris-tipo-documento"]').click()
            time.sleep(3)
            self.page.locator('.bs-searchbox input').click()
            time.sleep(3)
            self.page.locator('.bs-searchbox input').type(self.tipo_documento)
            time.sleep(3)
            self.page.locator(f'li:has-text("{self.tipo_documento}")').click()
            time.sleep(3)

            # Fazer upload do arquivo
            file_input = self.page.locator('#projuris-upload-input')
            file_input.set_input_files(name_file_main_download)
            time.sleep(10)

        except Exception as error:
            message = f"Erro ao inserir o arquivo '{name_file_main_download}' no Projuris."
            self.logger.message(message)
            raise error

        finally:
            # Remover o arquivo temporário baixado
            if os.path.exists(name_file_main_download):
                os.remove(name_file_main_download)

    def anexar_doc(self)-> None:
        try:
            #Documentos
            self.page.locator('#projuris\/ProcessoVO_3_obtem_tab__DocumentoProcessoprojuris\/ProcessoVO_3_obtem').click()
            #Adicionar Documento
            self.page.locator('#label_inclui-STATIC_projuris\/DocumentoProcessoVO_3_lista').click()
            #Adicionar Documento - Upload
            self.page.locator('#div-uploader > div > div.buttons > div').click()

            #############################Aqui precisa ser feito o upload do arquivo

            #Tipo Documento
            self.page.locator('#ID_TIPO_DOCUMENTOprojuris\/DocumentoProcessoVO_3_inclui').click()
            self.page.locator('#ID_TIPO_DOCUMENTOprojuris\/DocumentoProcessoVO_3_inclui').type(self.tipo_documento)
            time.sleep(2)   
            self.page.locator('#ID_TIPO_DOCUMENTOprojuris\/DocumentoProcessoVO_3_inclui_selectItem').first.click()
            #Data de Inclusão
            self.page.locator('#DATAprojuris\/DocumentoProcessoVO_3_inclui').click()
            self.page.locator('#DATAprojuris\/DocumentoProcessoVO_3_inclui').fill(self.data_inclusao_doc)
            #Salvar
            self.page.locator('#label_salvar-STATIC_projuris\/DocumentoProcessoVO_3_inclui').click()

        except ValueError as e:
            self.logger.message(f'Erro ao anexar documento: {e}')
        return 
