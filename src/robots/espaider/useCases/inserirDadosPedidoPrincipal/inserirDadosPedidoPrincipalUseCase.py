from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
from unidecode import unidecode
from robots.espaider.useCases.helpers.insertValueHelper import insert_value
from robots.espaider.useCases.helpers.selectOptionHelper import select_option

class InserirDadosPedidoPrincipalUseCase:
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
            "lkpPedidoEdt",
            "nbValorPedidoEdt",
        ]

        de_para = {
            "lkpPedidoEdt":"pedido_1",
            "nbValorPedidoEdt":"valor_pedido_1",
        }
        
        try:
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos Informação para a criação do pedido iniciado")
            for name in name_inputs:
                selected = False
                value = insert_value(data_input=self.data_input, de_para=de_para, name=name, frame=self.frame, tag="id")
                select = self.frame.wait_for_selector(f'#{name}')
                if not select:
                    raise(f'Erro ao preencher dados, campo: {name}')
                select.click()
                self.page.wait_for_timeout(2000)

                if name == 'nbValorPedidoEdt':
                    selected = True
                else:
                    select_option(page=self.page, name=name, value=value)

                if not selected:
                    raise(f'Erro ao preencher dados, campo: {name}')
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos Informação para a criação do pedido finalizado")
            return
        except Exception as e:
            message = e.args[0]
            self.classLogger.message(message)
            raise e