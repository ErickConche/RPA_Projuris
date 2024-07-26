from playwright.sync_api import Frame, Page
from modules.logger.Logger import Logger
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderExpModel import DadosEntradaEspaiderExpModel
from robots.espaider.useCases.helpers.insertValueHelper import insert_value
from robots.espaider.useCases.helpers.selectOptionHelper import select_option
from unidecode import unidecode

class CriarExpedienteUseCase:
    def __init__(self, page: Page, frame: Frame, data_input: DadosEntradaEspaiderExpModel, classLogger: Logger) -> None:
        self.page = page
        self.frame = frame
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        name_inputs = ["Desdobramento", "Evento", "DataEvento", "Observacoes"]
        de_para = {
            "Desdobramento": "processo",
            "Evento": "andamento",
            "DataEvento": "data_expediente",
            "Observacoes": "complementos"
        }

        try:
            self.classLogger.message("Iniciando criação do expediente")

            for name in name_inputs:
                self.classLogger.message(f"Processando campo: {name}")
                value = insert_value(data_input=self.data_input, de_para=de_para, name=name, frame=self.frame)
                self.fill_input(name, value)

            self.save_expediente()
        except Exception as e:
            self.classLogger.message(f"Erro ao criar expediente: {str(e)}")
            raise

    def fill_input(self, name: str, value: str):
        try:
            self.frame.wait_for_selector(f'[name={name}]').click()
            self.frame.wait_for_timeout(1000)

            if name == "Evento":
                select_option(page=self.page, name=name, value=value)
            elif name == "Desdobramento":
                instance = self.data_input.instancia
                
                options = self.page.query_selector_all('table > tbody > tr')
                
                if not options:
                    raise(f'Erro ao preencher dados, campo: {name}')

                selected = False

                for option in options:
                    td_option = option.query_selector_all('td')
                    option_text_1 = unidecode(td_option[3].inner_text()).lower()
                    option_text_2 = unidecode(td_option[1].inner_text()).lower()
                    if value == option_text_1 and instance in option_text_2:
                        option.dblclick()
                        selected = True
                        break
                if not selected:
                    raise Exception("Não foi selecionado nenhum desdobramento!")
                # self.page.get_by_text(value).dblclick()
            self.frame.wait_for_timeout(1000)
        except Exception as e:
            self.classLogger.message(f"Erro ao preencher o campo {name}: {str(e)}")
            raise

    def save_expediente(self):
        try:
            self.frame.wait_for_selector('button:has-text("SALVAR")').click()
            self.frame.wait_for_timeout(2000)
            self.classLogger.message("Expediente salvo com sucesso")
        except Exception as e:
            self.classLogger.message(f"Erro ao salvar o expediente: {str(e)}")
            raise