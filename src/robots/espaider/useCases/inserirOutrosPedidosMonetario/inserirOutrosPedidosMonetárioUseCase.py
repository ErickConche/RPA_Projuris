from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger

class InserirOutrosPedidosMonetárioUseCase:
    def __init__(
        self,
        page: Page,
        frame: Frame,
        data_input: DadosEntradaEspaiderModel,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.frame = frame
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        name_inputs = [
            "DataBase",
            "CLI_DataInicioVigencia"
        ]

        de_para = {
            "DataBase":"data_base_calculo",
            "CLI_DataInicioVigencia":"data_inicio_vigencia"
        }

        try:
            for name in name_inputs:
                value = getattr(self.data_input, de_para[name])
                self.frame.wait_for_selector(f"[name{name}]").fill(value)
        except Exception as e:
            raise e