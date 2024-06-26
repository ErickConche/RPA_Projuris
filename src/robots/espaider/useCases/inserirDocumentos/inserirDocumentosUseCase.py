from playwright.sync_api import Frame, Page
import requests
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
from unidecode import unidecode
import tempfile

class InserirDocumentosUseCase:
    def __init__(
        self,
        page: Page,
        frame: Frame,
        data_input: DadosEntradaEspaiderModel,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.frame = frame
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        name_inputs = [
            "NomeEdt",
            "Documento",
            "CLI_DataDocumento"
        ]

        de_para = {
            "NomeEdt":"nome_documento",
            "Documento":"file",
            "CLI_DataDocumento":"data_documento"
        }
        
        try:
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos documentos do processo [outros] iniciado")
            for name in name_inputs:
                value = getattr(self.data_input, de_para[name])
                
                if name == "NomeEdt":
                    self.frame.wait_for_selector(f"#{name}").fill(value)
                elif name == "CLI_DataDocumento":
                    self.frame.wait_for_selector(f"[name={name}]").fill(value)
                elif name == "Documento":
                    input_selector = f"[id=Documento_file]"
                    file = self.download_file(url=value)
                    self.frame.set_input_files(input_selector, file)

            self.frame.click("#bm-Save")
            self.frame.wait_for_load_state("networkidle")
            self.frame.wait_for_timeout(5000)
            self.frame.wait_for_selector("#Close")
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos documentos do processo [outros] finalizado")
            return
        except Exception as e:
            message = e.args[0]
            self.classLogger.message(message)
            raise e

    def download_file(self, url):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file_name = temp_file.name
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=8192):
                temp_file.write(chunk)
        temp_file.close()
        return temp_file_name