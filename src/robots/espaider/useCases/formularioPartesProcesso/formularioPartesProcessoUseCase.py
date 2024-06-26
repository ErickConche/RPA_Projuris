from playwright.sync_api import Page, Frame
from modules.logger.Logger import Logger
import re
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from robots.espaider.useCases.inserirOutrasPartes.inserirOutrasPartesUseCase import (
    InserirOutrasPartesUseCase)
from robots.espaider.useCases.inserirOutrosPedidos.inserirOutrosPedidosUseCase import (
    InserirOutrosPedidosUseCase)
from robots.espaider.useCases.inserirDocumentos.inserirDocumentosUseCase import (
    InserirDocumentosUseCase)

class FormularioPartesProcessoUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderModel,
        classLogger: Logger,
        data_output
    ):
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        try:
            frame_main = self.set_frame()

            regex = r'parte_contraria_\w+'
            pedidos_instance = dir(self.data_input)
            pedidos = [attr for attr in pedidos_instance if re.match(regex, attr)]

            partes_indices = []

            for index, pedido in enumerate(pedidos):
                value = getattr(self.data_input, pedido)
                if not value:
                    continue
                indice = pedido.split('_')[-1]
                partes_indices.append(indice)

            if partes_indices:
                frame = self.change_frame(frame_main=frame_main, tab="Partes do processo")

                '''
                *** Partes do processo ***
                '''
                for i in partes_indices:
                    InserirOutrasPartesUseCase(
                        page=self.page,
                        frame=frame,
                        data_input=self.data_input, 
                        classLogger=self.classLogger
                    ).execute(indice=i)

            '''
            *** Pedidos ***
            '''

            regex = r'pedido_\w+'
            pedidos_instance = dir(self.data_input)
            pedidos = [attr for attr in pedidos_instance if re.match(regex, attr)]

            pedido_indices = []

            for index, pedido in enumerate(pedidos):
                value = getattr(self.data_input, pedido)
                if index == 0:
                    continue
                if not value:
                    continue
                indice = pedido.split('_')[-1]
                pedido_indices.append(indice)

            if pedido_indices:
                frame = self.change_frame(frame_main=frame_main, tab="Pedidos")

                for i in pedido_indices:
                    InserirOutrosPedidosUseCase(
                        page=self.page,
                        frame=frame,
                        data_input=self.data_input, 
                        classLogger=self.classLogger
                    ).execute(indice=i)

            if self.data_input.file:
                '''
                *** Documentos ***
                '''

                frame = self.change_frame(frame_main=frame_main, tab="Documentos")

                InserirDocumentosUseCase(
                    page=self.page,
                    frame=frame,
                    data_input=self.data_input, 
                    classLogger=self.classLogger
                ).execute()

        except Exception as e:
            raise e

    def set_frame(self) -> Frame:
        frame = None
        
        self.page.wait_for_selector('iframe')
        frames = self.page.query_selector_all('iframe')
        
        if frames:
            last_frame = frames[-1]
            
            frame_name = last_frame.get_attribute('name')
            frame_id = last_frame.get_attribute('id')
            
            if frame_name or frame_id:
                frame = self.page.frame(name=frame_name) if frame_name else self.page.frame(id=frame_id)

        return frame

    def change_frame(self, frame_main: Frame, tab) -> Frame:
        frame_main.wait_for_selector(f'button:has-text("{tab}")').click()
        frame_main.wait_for_timeout(2000)

        frame_main_top = frame_main.child_frames.pop()
        
        frame_main_top.get_by_text("Novo").click()

        return self.set_frame()