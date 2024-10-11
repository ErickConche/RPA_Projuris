import time
from modules.logger.Logger import Logger
from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderCadastroModel import DadosEntradaEspaiderCadastroModel
from robots.espaider.useCases.inserirAudienciaDesignada.inserirAudienciaDesignadaUseCase import InserirAudienciaDesignadaUseCase


class FormularioGpaAreasUseCase:
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
            *** GPA/ÁREAS ***
            '''
            self.classLogger.message('Iniciando cadastro das informações da aba de GPA/Áreas')
            time.sleep(5)
            iframe_list = self.page.query_selector_all('iframe')
            iframe_name = iframe_list[len(iframe_list)-1].get_attribute('name')
            desdobramento_iframe = self.page.frame(name=iframe_name)
            desdobramento_iframe.query_selector('[class="x-tab x-tab-text x-item x-tab-bottom x-ripple-effect--target"]:has-text("GPA/Áreas")').click()
            time.sleep(5)
            iframe_list = desdobramento_iframe.query_selector_all('iframe')
            iframe_name = iframe_list[len(iframe_list)-1].get_attribute('name')
            add_gpa_iframe = self.page.frame(name=iframe_name)
            add_gpa_iframe.query_selector('button[data-icon="add_circle"]').click()
            time.sleep(3)
            iframe_list = self.page.query_selector_all('iframe')
            iframe_name = iframe_list[len(iframe_list)-1].get_attribute('name')
            gpa_iframe = self.page.frame(name=iframe_name)
            gpa_iframe.query_selector('[name="CLI_GPAComplexo"]').type(self.data_input.complexo)
            time.sleep(4)
            input_list = self.page.query_selector_all(f'[title="{self.data_input.complexo}"]')
            last_input = input_list[len(input_list)-1]
            last_input.dblclick()
            actual_input_len = len(input_list)
            time.sleep(4)
            gpa_iframe.query_selector('[name="CLI_GPAMinaUnidade"]').type(self.data_input.mina_unidade)
            time.sleep(4)
            input_list = self.page.query_selector_all(f'[title="{self.data_input.mina_unidade}"]>div:has-text("{self.data_input.mina_unidade}")')
            last_input = input_list[actual_input_len]
            last_input.dblclick()
            time.sleep(4)
            gpa_iframe.query_selector('button[id="bm-Save"]').click()
            if self.data_input.audiencia_designada:
                self.classLogger.message('Cadastrando Audiencia Designada')
                InserirAudienciaDesignadaUseCase(
                    page=self.page,
                    data_input=self.data_input,
                    classLogger=self.classLogger,
                    robot=self.robot,
                    iframe=gpa_iframe
                ).execute()
                time.sleep(10)
                iframe_list = self.page.query_selector_all('iframe')
                iframe_name = iframe_list[len(iframe_list)-1].get_attribute('name')
                close_iframe = self.page.frame(name=iframe_name)
                close_iframe.query_selector('[id="Close"]').click()
                time.sleep(5)
                iframe_name = gpa_iframe.query_selector('iframe').get_attribute('name')
                close_iframe = self.page.frame(name=iframe_name)
                close_iframe.query_selector('[title="Sair"]').click()
                time.sleep(2)
                iframe_list = self.page.query_selector_all('iframe')
                iframe_name = iframe_list[len(iframe_list)-1].get_attribute('name')
                home_iframe = self.page.frame(name=iframe_name)
                home_iframe.query_selector('[data-icon="home"]').click()
                time.sleep(5)
            return {
                'status': True,
                'iframe': home_iframe
            }
        except Exception as e:
            print(str(e))
            raise Exception("Erro ao preencher os dados da aba GPA/ÁREAS")
