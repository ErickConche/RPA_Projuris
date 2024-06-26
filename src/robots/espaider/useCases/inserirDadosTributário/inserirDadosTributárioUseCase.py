from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
from unidecode import unidecode
from robots.espaider.useCases.helpers.insertValueHelper import insert_value
from robots.espaider.useCases.helpers.selectOptionHelper import select_option

class InserirDadosTributárioUseCase:
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
            "RegraAtualizacao",
            "DataInicioContabil",
            "CLI_DataInicioVigencia",
            "ValorOriginalTributo",
            "ValorOriginalMulta",
            "VlJurosTributo",
            "DataBase",
            "DataBaseMulta",
            "DataBaseJuros",
            "ValorRiscoOriginalTributo",
            "ValorRiscoOriginalMulta",
            "ValorRiscoOriginalJuros"
        ]

        de_para = {
            "RegraAtualizacao":"regra",
            "DataInicioContabil":"data_inicio_contabil",
            "CLI_DataInicioVigencia":"data_inicio_vigencia",
            "ValorOriginalTributo":"valor_tributo",
            "ValorOriginalMulta":"valor_multa",
            "VlJurosTributo":"valor_juros",
            "DataBase":"data_distribuicao",
            "DataBaseMulta":"data_distribuicao",
            "DataBaseJuros":"data_distribuicao",
            "ValorRiscoOriginalTributo":"valor_tributo",
            "ValorRiscoOriginalMulta":"valor_multa",
            "ValorRiscoOriginalJuros":"valor_juros"
        }

        try:
            for name in name_inputs:
                value = insert_value(data_input=self.data_input, de_para=de_para, name=name, frame=self.frame)
                if name != 'RegraAtualizacao':
                    continue
                self.frame.wait_for_selector(f"name={name}").click()
                self.frame.wait_for_timeout(2000)

                select_option(page=self.page, name=name, value=value)
            return
        except Exception as e:
            raise e