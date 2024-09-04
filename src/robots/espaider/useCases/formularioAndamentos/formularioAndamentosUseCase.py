import time
from modules.logger.Logger import Logger
from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderCadastroModel import DadosEntradaEspaiderCadastroModel


class FormularioAndamentosUseCase:
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
            *** Informações Andamentos ***
            '''
            self.classLogger.message('Iniciando cadastro das informações dos Andamentos')
            time.sleep(5)
            self.iframe.query_selector('[class="x-tab x-tab-text x-item x-tab-bottom x-ripple-effect--target"]:has-text("Andamentos")').click()
            time.sleep(2)
            iframe_list = self.iframe.query_selector_all('iframe')
            iframe_name = iframe_list[len(iframe_list)-1].get_attribute('name')
            add_iframe = self.page.frame(name=iframe_name)
            add_iframe.query_selector('[data-icon="add_circle"]').click()
            time.sleep(2)
            iframe_list = self.page.query_selector_all('iframe')
            iframe_name = iframe_list[len(iframe_list)-1].get_attribute('name')
            info_andamentos_iframe = self.page.frame(name=iframe_name)
            info_andamentos_iframe.query_selector('[name="Desdobramento"]').type(self.data_input.numero_do_processo)
            time.sleep(2)
            self.page.query_selector(f'[title="{self.data_input.numero_do_processo}"]').dblclick()
            time.sleep(2)
            info_andamentos_iframe.query_selector('[name="Evento"]').type(self.data_input.andamento)
            time.sleep(2)
            self.page.query_selector(f'[title="{self.data_input.andamento}"]').dblclick()
            time.sleep(2)
            info_andamentos_iframe.query_selector('[name="DataEvento"]').fill('')
            info_andamentos_iframe.query_selector('[name="DataEvento"]').type(self.data_input.data_andamento)
            time.sleep(2)
            info_andamentos_iframe.query_selector('[data-icon="save"]').dblclick()
            time.sleep(2)
            info_andamentos_iframe.query_selector('[title="Sair"]').click()
            return {
                'status': True
            }
        except Exception as e:
            print(str(e))
            raise Exception("Erro ao preencher os dados dos Andamentos")
