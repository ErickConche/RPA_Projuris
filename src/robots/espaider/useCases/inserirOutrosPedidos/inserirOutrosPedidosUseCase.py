from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
from unidecode import unidecode
from robots.espaider.useCases.helpers.selectOptionHelper import select_option

class InserirOutrosPedidosUseCase:
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

    def execute(self, indice):
        name_inputs = [
            "Pedido",
            "ValorPagoOriginal"
        ]

        de_para = {
            "Pedido":"",
            "ValorPagoOriginal":""
        }
        
        try:
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos pedidos do processo [outros] iniciado")
            for name in name_inputs:
                de_para.update({
                    "Pedido":f"pedido_{indice}",
                    "ValorPagoOriginal":f"valor_pedido_{indice}"
                })
                
                selected = False
                value = getattr(self.data_input, de_para[name])
                self.frame.wait_for_selector(f"[name{name}]").fill(value)
                if name == "ValorPagoOriginal":
                    continue
                self.frame.wait_for_selector(f"[name{name}]").click()
                selected = select_option(page=self.page, name=name, value=value)
                
                if not selected:
                        raise(f'Erro ao preencher dados, campo: {name}')

            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos pedidos do processo [outros] finalizado")
            ###
            self.frame.wait_for_selector("#bm-Save").click()
            self.frame.wait_for_timeout(2000)
            
            self.frame.wait_for_selector("#Close")
            return
        except Exception as e:
            message = e.args[0]
            self.classLogger.message(message)
            raise e