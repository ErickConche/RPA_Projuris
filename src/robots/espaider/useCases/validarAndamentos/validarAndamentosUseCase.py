from datetime import datetime
from playwright.sync_api import ElementHandle, Frame, Page
from modules.logger.Logger import Logger
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderExpModel import (
    DadosEntradaEspaiderExpModel)

class ValidarAndamentosUseCase:
    def __init__(
        self, 
        page: Page,
        frame: Frame,
        data_input: DadosEntradaEspaiderExpModel,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.frame = frame
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self) -> bool:
        try:
            progress_search_name = self.data_input.andamento.lower()
            progress_search_date = self.data_input.data_expediente
            if len(self.data_input.data_expediente.split('/')[-1]) == 2:
                progress_search_date = datetime.strptime(self.data_input.data_expediente, '%d/%m/%y').strftime('%d/%m/%Y')

            list_progress = self.frame.query_selector_all('table > tbody > tr')

            for progress in list_progress:
                tds = progress.query_selector_all('td')
                progress_td_name_value = tds[1].inner_text().lower()
                progress_td_date_value = tds[3].inner_text()

                if (progress_td_name_value == progress_search_name and 
                    progress_td_date_value == progress_search_date):
                    return True
            else:
                return False
        except Exception as e:
            raise Exception("Erro ao executar a busca de expedientes do processo")
