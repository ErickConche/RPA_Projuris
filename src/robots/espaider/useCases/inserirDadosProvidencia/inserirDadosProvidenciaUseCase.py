from playwright.sync_api import Frame, Page
from modules.logger.Logger import Logger
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderExpModel import DadosEntradaEspaiderExpModel
from robots.espaider.useCases.helpers.insertValueHelper import insert_value
from robots.espaider.useCases.helpers.selectOptionHelper import select_option

class InserirDadosProvidenciaUseCase:
    def __init__(self, page: Page, frame: Frame, data_input: DadosEntradaEspaiderExpModel, classLogger: Logger) -> None:
        self.page = page
        self.frame = frame
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        name_inputs = ["Providencia", "Responsavel", "DataInicio"]
        data_hora = f"{self.data_input.data_audiencia} {self.data_input.hora_audiencia}"
        de_para = {"Providencia": "compromisso"}

        try:
            self.classLogger.message("Iniciando inserção de dados de providência")
            for name in name_inputs:
                self.classLogger.message(f"Processando campo: {name}")
                if name == "Providencia":
                    self.process_providencia(name, de_para)
                elif name == "Responsavel":
                    self.process_responsavel(name)
                else:
                    self.process_data_inicio(name, data_hora)
            self.process_save()
            self.classLogger.message("Inserção de dados de providência concluída com sucesso")
        except Exception as e:
            self.classLogger.message(f"Erro ao inserir dados de providência: {str(e)}")
            raise

    def process_providencia(self, name: str, de_para: dict):
        try:
            value = insert_value(data_input=self.data_input, de_para=de_para, name=name, frame=self.frame)
            self.frame.wait_for_selector(f'[name={name}]').click()
            self.frame.wait_for_timeout(1000)
            select_option(page=self.page, name=name, value=value)
            self.frame.wait_for_timeout(1000)
        except Exception as e:
            self.classLogger.message(f"Erro ao processar campo {name}: {str(e)}")
            raise

    def process_responsavel(self, name: str):
        try:
            self.frame.wait_for_selector(f'[name={name}]').click()
            table_element = self.page.query_selector_all('table > tbody')[-1]
            table_element.query_selector('tr').click()
            self.frame.wait_for_timeout(1000)
        except Exception as e:
            self.classLogger.message(f"Erro ao processar campo {name}: {str(e)}")
            raise

    def process_data_inicio(self, name: str, data_hora: str):
        try:
            self.frame.wait_for_selector(f'[name={name}]').fill(data_hora)
        except Exception as e:
            self.classLogger.message(f"Erro ao processar campo {name}: {str(e)}")
            raise

    def process_save(self):
        try:
            self.frame.wait_for_selector('button:has-text("SALVAR")').click()
            self.frame.wait_for_timeout(2000)
            self.classLogger.message("Providência salva com sucesso")
            self.frame.wait_for_selector('#Close').click()
        except Exception as e:
            self.classLogger.message(f"Erro ao salvar a providência: {str(e)}")
            raise
