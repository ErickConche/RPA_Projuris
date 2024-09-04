import os
import time
from modules.logger.Logger import Logger
from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderCadastroModel import DadosEntradaEspaiderCadastroModel


# ABA DOCUMENTOS E IMAGENS
class FormularioArquivosUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderCadastroModel,
        classLogger: Logger,
        robot: str,
        iframe: Frame
    ):
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.robot = robot
        self.iframe = iframe

    def execute(self):
        try:
            '''
            *** Informações Documentos e Imagens ***
            '''
            self.classLogger.message('Iniciando cadastro das informações da aba de Arquivos')
            time.sleep(10)
            self.iframe.query_selector('[class="x-tab x-tab-text x-item x-tab-bottom x-ripple-effect--target"]:has-text("Documentos e Imagens")').click()
            time.sleep(10)
            if self.page.query_selector('tour-popup') and self.page.query_selector('tour-popup').is_visible():
                self.page.query_selector('tour-popup > tour-popup-actions > button > check-icon').click()
                time.sleep(3)
            name_iframe = self.iframe.query_selector('iframe').get_attribute('name')
            add_arquivos_iframe = self.page.frame(name_iframe)
            add_arquivos_iframe.query_selector('[data-icon="add_circle"]').click()
            list_iframe = self.page.query_selector_all('iframe')
            name_iframe = list_iframe[len(list_iframe)-1].get_attribute('name')
            arquivos_iframe = self.page.frame(name_iframe)
            time.sleep(3)
            arquivos_iframe.query_selector('[name="Nome"]').type(self.data_input.nome_assunto)
            arquivos_iframe.query_selector('[name="CLI_TipoDocumento"]').type(self.data_input.tipo_documento)
            time.sleep(2)
            self.page.query_selector(f'[title="{self.data_input.tipo_documento}"]').click()
            with self.page.expect_file_chooser() as fc_info:
                arquivos_iframe.query_selector('[name="Documento"]').click()
            file_chooser = fc_info.value
            file_chooser.set_files(os.path.join(os.getcwd(), self.data_input.arquivo))
            time.sleep(7)
            arquivos_iframe.query_selector('[id="bm-Save"]').click()
            time.sleep(4)
            arquivos_iframe.query_selector('[id="Close"]').click()
            time.sleep(2)
            add_arquivos_iframe.query_selector('[title="Sair"]').click()
            return {
                'status': True,
                'iframe': self.iframe
            }
        except Exception as e:
            print(str(e))
            raise Exception("Erro ao preencher os dados dos Arquivos")
