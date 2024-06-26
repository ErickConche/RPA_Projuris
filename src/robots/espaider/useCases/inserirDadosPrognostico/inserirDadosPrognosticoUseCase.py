from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
from unidecode import unidecode
from robots.espaider.useCases.helpers.selectOptionHelper import select_single
from robots.espaider.useCases.helpers.insertValueHelper import insert_value

class InserirDadosPrognosticoUseCase:
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
            "DataBaseCalculo",
            "CLI_DataInicioVigencia",
            "DataInicioContabil",
            "RiscoOriginal",
            "CLI_Inestimavel"
        ]

        de_para = {
            "DataBaseCalculo":"data_base_calculo",
            "CLI_DataInicioVigencia":"data_inicio_vigencia",
            "DataInicioContabil":"data_inicio_contabil",
            "RiscoOriginal":"risco_original",
            "CLI_Inestimavel":"inestimavel"
        }
        
        try:
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos Valores | Prognóstico iniciado")
            for name in name_inputs:
                selected = False
                value = insert_value(data_input=self.data_input, de_para=de_para, name=name, frame=self.frame)
                self.page.wait_for_timeout(2000)
                if name in [ "DataBaseCalculo", "CLI_DataInicioVigencia", "DataInicioContabil"]:
                    continue
                self.frame.wait_for_selector(f'[name={name}]').click()

                select_single(page=self.page, value=value)
                
                if not selected:
                    raise(f'Erro ao preencher dados, campo: {name}')
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos Valores | Prognóstico finalizado")
            return
        except Exception as e:
            message = e.args[0]
            self.classLogger.message(message)
            raise e