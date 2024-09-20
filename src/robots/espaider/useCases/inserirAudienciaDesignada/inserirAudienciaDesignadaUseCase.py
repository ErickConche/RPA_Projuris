import time
from modules.logger.Logger import Logger
from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderCadastroModel import DadosEntradaEspaiderCadastroModel
from robots.espaider.useCases.inserirJuizo.inserirJuizoUseCase import InserirJuizoUseCase
from robots.espaider.useCases.helpers.selectOptionHelper import select_option,select_single


# CADASTRO DE JUÍZO
class InserirAudienciaDesignadaUseCase:
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
            *** Cadastro de Audiência Designada ***
            '''
            self.classLogger.message('Iniciando cadastro de Audiência Designada')
            time.sleep(5)
            self.iframe.query_selector('[class="x-tab x-tab-text x-item x-tab-bottom x-ripple-effect--target"]:has-text("GPA Providências")').click()
            time.sleep(5)
            iframe_list = self.iframe.query_selector_all('iframe')
            iframe_name = iframe_list[len(iframe_list)-1].get_attribute('name')
            add_gpa_providencias_iframe = self.page.frame(name=iframe_name)
            add_gpa_providencias_iframe.query_selector('button[data-icon="add_circle"]').click()
            time.sleep(4)
            iframe_list = self.page.query_selector_all('iframe')
            iframe_name = iframe_list[len(iframe_list)-1].get_attribute('name')
            gpa_providencias_iframe = self.page.frame(name=iframe_name)
            gpa_providencias_iframe.query_selector('[name="CLI_GPAAndamento"]').type(self.data_input.em_andamento)
            time.sleep(2)
            select_option(page=self.page, name="CLI_GPAAndamento", value=self.data_input.em_andamento)
            time.sleep(2)
            gpa_providencias_iframe.query_selector('[name="CLI_TipoAudiencia"]').type(self.data_input.tipo_audiencia)
            time.sleep(2)
            select_option(page=self.page, name="CLI_TipoAudiencia", value=self.data_input.tipo_audiencia)
            time.sleep(2)
            gpa_providencias_iframe.query_selector('[name="CLI_Modalidade"]').type(self.data_input.modalidade)
            time.sleep(2)
            select_option(page=self.page, name="CLI_Modalidade", value=self.data_input.modalidade)
            time.sleep(2)
            gpa_providencias_iframe.query_selector('[name="CLI_GPAHora"]').type(self.data_input.hora_audiencia)
            time.sleep(2)
            gpa_providencias_iframe.query_selector('[name="CLI_GPAProvidencia"]').type(self.data_input.providencia_audiencia)
            time.sleep(2)
            select_option(page=self.page, name="CLI_GPAProvidencia", value=self.data_input.providencia_audiencia)
            time.sleep(2)
            gpa_providencias_iframe.query_selector('[name="CLI_GPAResponsavel"]').type(self.data_input.responsavel_audiencia)
            time.sleep(2)
            input_list = self.page.query_selector_all(f'[title="{self.data_input.responsavel_audiencia}"]')
            responsavel_input = input_list[len(input_list)-1]
            responsavel_input.dblclick()
            time.sleep(2)
            gpa_providencias_iframe.query_selector('[name="CLI_GPADataAlerta"]').type(self.data_input.alerta_prazo_audiencia)
            time.sleep(2)
            gpa_providencias_iframe.query_selector('[name="CLI_GPADataInicial"]').type(self.data_input.distribuido_em)
            time.sleep(2)
            gpa_providencias_iframe.query_selector('[name="CLI_GPAVara"]').type(self.data_input.vara)
            time.sleep(2)
            if self.data_input.vara:
                select_option(page=self.page, name="CLI_GPAVara", value=self.data_input.vara)
            time.sleep(2)
            gpa_providencias_iframe.query_selector('[name="CLI_GPAComarca"]').type(self.data_input.comarca)
            time.sleep(5)
            select_option(page=self.page, name="CLI_GPAComarca", value=self.data_input.comarca)
            time.sleep(2)
            gpa_providencias_iframe.query_selector('[name="CLI_Status"]').type(self.data_input.status_audiencia)
            time.sleep(2)
            select_single(page=self.page, value=self.data_input.status_audiencia)
            time.sleep(2)
            gpa_providencias_iframe.query_selector('[name="CLI_GPAJuizo"]').type(self.data_input.juizo)
            time.sleep(5)
            if not select_option(page=self.page, name="CLI_GPAJuizo", value=self.data_input.juizo):
                InserirJuizoUseCase(
                    page=self.page,
                    data_input=self.data_input,
                    classLogger=self.classLogger,
                    robot=self.robot,
                    iframe=gpa_providencias_iframe,
                    juiz_selector='[name="CLI_GPAJuizo"]'
                ).execute()
            gpa_providencias_iframe.query_selector('[id="bm-Save"]').click()
        except Exception as e:
            raise e
