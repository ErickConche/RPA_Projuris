import time
from modules.logger.Logger import Logger
from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderCadastroModel import DadosEntradaEspaiderCadastroModel
from robots.espaider.useCases.helpers.selectOptionHelper import select_option


# CADASTRO DE JUÍZO
class InserirJuizoUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderCadastroModel,
        classLogger: Logger,
        robot: str,
        iframe: Frame,
        juiz_selector: str
    ):
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.robot = robot
        self.iframe = iframe
        self.juiz_selector = juiz_selector

    def execute(self):
        try:
            '''
            *** Cadastro de Juízo ***
            '''
            self.classLogger.message('Iniciando cadastro do Juízo')
            inserted = False
            time.sleep(5)
            self.page.query_selector('[class="x-popup x-anim-fade x-popup-grid-menu x-elevation-z8 x-layout--container"] > div > div > div > div > button[data-icon="add_circle"]').click()
            time.sleep(4)
            iframe_list = self.page.query_selector_all('iframe')
            cadastro_juizo_iframe_name = iframe_list[len(iframe_list)-1].get_attribute('name')
            cadastro_juizo_iframe = self.page.frame(name=cadastro_juizo_iframe_name)
            cadastro_juizo_iframe.query_selector('[name="Nome"]').type(self.data_input.juizo)
            cadastro_juizo_iframe.query_selector('[name="Comarca"]').type(self.data_input.comarca)
            time.sleep(5)
            select_option(page=self.page, name="Comarca", value=self.data_input.comarca)
            time.sleep(3)
            cadastro_juizo_iframe.query_selector('[id="bm-Save"]').click()
            time.sleep(3)
            cadastro_juizo_iframe.query_selector('[id="Close"]').click()
            time.sleep(2)
            self.iframe.query_selector(self.juiz_selector).fill('')
            time.sleep(2)
            self.iframe.query_selector(self.juiz_selector).type(self.data_input.juizo)
            time.sleep(3)
            if select_option(page=self.page, name="Juizo", value=self.data_input.juizo):
                inserted = True
                self.classLogger.message(f'Juízo {self.data_input.juizo} inserido com sucesso!')
            return inserted
        except Exception as e:
            print(str(e))
            raise Exception("Erro ao cadastro o Juízo")
