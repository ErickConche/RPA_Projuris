import time
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderCadastroModel import DadosEntradaEspaiderCadastroModel


class PesquisarProcessoUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderCadastroModel,
        classLogger: Logger,
    ):
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        try:
            self.classLogger.message('Pesquisando processo')
            time.sleep(2)
            find_process = False
            process_row = ''
            iframe_name = self.page.query_selector('[class="x-simpleiframe x-item"]').get_attribute('name')
            iframe = self.page.frame(name=iframe_name)
            iframe.query_selector('[placeholder="Pesquisar"]').type(self.data_input.numero_processo_pre_cadastro)
            self.page.keyboard.press("Enter")
            time.sleep(15)
            table_rows = iframe.query_selector_all('tbody>tr')
            header_list = iframe.query_selector_all('[role="columnheader"]')
            for row in table_rows:
                if row.query_selector(f'td[title="{self.data_input.numero_processo_pre_cadastro}"]'):
                    find_process = True
                    process_row = row
                    break
            return {
                "LinhaProcesso": process_row,
                "ProcessoEncontrado": find_process,
                "HeaderList": header_list,
                "Iframe": iframe,
                "Status": True
            }
        except Exception as e:
            print(str(e))
            raise Exception("Erro ao buscar o processo")
