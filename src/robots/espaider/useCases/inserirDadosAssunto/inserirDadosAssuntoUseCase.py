from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger


class InserirDadosAssuntoUseCase:
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
        try:
            self.classLogger.message("[Espaider-Civil]: Preenchimento do campo Descrição assunto | Principais objetos iniciado")
            value = self.data_input.descricao_assunto
            if self.data_input.categoria == 'Trabalhista':
                value = value.replace(",", "\n")
            self.frame.wait_for_selector('#DetalhamentoEdt').fill(value)
            self.classLogger.message("[Espaider-Civil]: Preenchimento do campo Descrição assunto | Principais objetos finalizado")
        except Exception as e:
            self.classLogger.message(e.args[0])
            raise e
