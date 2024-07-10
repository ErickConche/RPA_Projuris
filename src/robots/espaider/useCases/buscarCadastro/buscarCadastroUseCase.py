from playwright.sync_api import ElementHandle, Frame, Page
from modules.logger.Logger import Logger
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderExpModel import DadosEntradaEspaiderExpModel

class BuscarCadastroUseCase:
    def __init__(self, page: Page, frame: Frame, data_input: DadosEntradaEspaiderExpModel, classLogger: Logger) -> None:
        self.page = page
        self.frame = frame
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self) -> ElementHandle:
        try:
            self.classLogger.message("Iniciando busca de cadastro")
            processo = self.data_input.processo
            self.frame.wait_for_timeout(2000)

            input_field = self.find_input_field('Número')
            if input_field:
                input_field.fill(processo)
                input_field.press('Enter')
                self.frame.wait_for_timeout(5000)

            process = self.frame.wait_for_selector('table > tbody > tr', timeout=10000)
            if process:
                self.classLogger.message("Processo encontrado")
                return process
            else:
                self.classLogger.message("Processo não encontrado")
                return None
        except Exception as e:
            self.classLogger.message(f"Erro ao buscar cadastro: {str(e)}")
            return None

    def find_input_field(self, label_text: str) -> ElementHandle:
        """Procura e retorna o campo de entrada correspondente ao texto do rótulo fornecido."""
        try:
            selector = '.x-form.x-item.x-form--outlined.x-textfield'
            elements = self.frame.query_selector_all(selector)
            for element in elements:
                label = element.query_selector('label')
                if label and label.inner_text() == label_text:
                    return element.query_selector('input')
            self.classLogger.message(f"Campo de entrada com o rótulo '{label_text}' não encontrado")
            return None
        except Exception as e:
            self.classLogger.message(f"Erro ao procurar campo de entrada: {str(e)}")
            return None
