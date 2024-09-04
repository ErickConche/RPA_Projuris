import time
from modules.logger.Logger import Logger
from playwright.sync_api import Frame, Page
from robots.espaider.useCases.inserirJuizo.inserirJuizoUseCase import InserirJuizoUseCase
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderCadastroModel import DadosEntradaEspaiderCadastroModel


# ABA VALOR
class FormularioValorUseCase:
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
            *** Informações Tópico Geral ***
            '''
            self.classLogger.message('Iniciando cadastro das informações da aba de Valores')
            time.sleep(5)
            self.iframe.query_selector('[class="x-tab x-tab-text x-item x-ripple-effect--target"]:has-text("Valores")').click()
            self.iframe.query_selector('[name="ValorCausa"]').fill('')
            self.iframe.query_selector('[name="ValorCausa"]').type(self.data_input.valor_da_causa)
            time.sleep(2)
            self.iframe.query_selector('[id="bm-Save"]').click()
            time.sleep(5)
            self.iframe.query_selector('[class="x-tab x-tab-text x-item x-tab-bottom x-ripple-effect--target"]:has-text("Desdobramentos")').click()
            time.sleep(7)
            if self.page.query_selector('tour-popup') and self.page.query_selector('tour-popup').is_visible():
                self.page.query_selector('tour-popup > tour-popup-actions > button > check-icon').click()
            name_iframe = self.iframe.query_selector('[id="colDesdobramentos"]>div>iframe').get_attribute('name')
            novo_desdobramento_iframe = self.page.frame(name=name_iframe)
            novo_desdobramento_iframe.query_selector('[class="x-btn x-btn-text x-item x-ripple-effect--target"]:has-text("Novo")').click()
            list_iframe_page = self.page.query_selector_all('iframe')
            name_iframe = self.page.query_selector_all('iframe')[len(list_iframe_page)-1].get_attribute('name')
            desdobramento_iframe = self.page.frame(name_iframe)
            time.sleep(5)
            desdobramento_iframe.query_selector('[name="Desdobramento"]').type(self.data_input.desdobramento)
            time.sleep(5)
            self.page.query_selector(f'[title="{self.data_input.desdobramento}"]').dblclick()
            time.sleep(2)
            desdobramento_iframe.query_selector('[name="Rito"]').type(self.data_input.procedimento)
            time.sleep(2)
            self.page.query_selector(f'[title="{self.data_input.procedimento}"]').dblclick()
            time.sleep(2)
            desdobramento_iframe.query_selector('[name="Instancia"]').type(self.data_input.instancia)
            time.sleep(2)
            list_selectors = self.page.query_selector_all(f'[title="{self.data_input.instancia}"]')
            list_selectors[len(list_selectors)-1].dblclick()
            time.sleep(2)
            desdobramento_iframe.query_selector('[name="Orgao"]').type(self.data_input.orgao)
            time.sleep(4)
            self.page.query_selector(f'[title="{self.data_input.orgao}"]').dblclick()
            time.sleep(2)
            desdobramento_iframe.query_selector('[name="Comarca"]').type(self.data_input.comarca)
            time.sleep(3)
            self.page.query_selector(f'[title="{self.data_input.comarca}"]').dblclick()
            time.sleep(3)
            desdobramento_iframe.query_selector('[name="Numero"]').click()
            desdobramento_iframe.query_selector('[name="Numero"]').type(self.data_input.numero_do_processo)
            time.sleep(2)
            desdobramento_iframe.query_selector('[name="Juizo"]').type(self.data_input.juizo)
            time.sleep(3)
            if self.page.query_selector(f'[title="{self.data_input.juizo}"]'):
                self.page.query_selector(f'[title="{self.data_input.juizo}"]').dblclick()
            else:
                InserirJuizoUseCase(
                    page=self.page,
                    data_input=self.data_input,
                    classLogger=self.classLogger,
                    robot=self.robot,
                    iframe=desdobramento_iframe,
                    juiz_selector='[name="Juizo"]'
                ).execute()
            time.sleep(2)
            desdobramento_iframe.query_selector('[name="DataDistribuicao"]').type(self.data_input.distribuido_em)
            time.sleep(2)
            desdobramento_iframe.query_selector('[id="bm-Save"]').click()
            time.sleep(2)
            if self.page.query_selector('[id="messagebox"]') and 'mesmo assim' in self.page.query_selector('[id="messagebox"]>div').inner_text():
                self.classLogger.message('Desdobramento ja cadastrado')
                self.page.query_selector('[id="messagebox"]>div>div>button:has-text("OK")').click()
            time.sleep(10)
            return {
                'status': True,
                'iframe': desdobramento_iframe
            }
        except Exception as e:
            print(str(e))
            raise Exception("Erro ao preencher dados dos valores")
