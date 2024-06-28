from datetime import datetime
from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderExpModel import (
    DadosEntradaEspaiderExpModel)
from modules.logger.Logger import Logger
from robots.espaider.useCases.buscarCadastro.buscarCadastroUseCase import BuscarCadastroUseCase
from robots.espaider.useCases.validarAndamentos.validarAndamentosUseCase import ValidarAndamentosUseCase
from robots.espaider.useCases.criarExpediente.criarExpedienteUseCase import CriarExpedienteUseCase
from robots.espaider.useCases.inserirDadosProvidencia.inserirDadosProvidenciaUseCase import InserirDadosProvidenciaUseCase


class AndamentoUseCase:
    def __init__(self, page: Page, data_input: DadosEntradaEspaiderExpModel, classLogger: Logger, robot: str):
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.robot = robot

    def execute(self):
        try:
            self.classLogger.message("Iniciando o processo de andamento")
            frame_main = self.set_frame()

            process = BuscarCadastroUseCase(page=self.page, frame=frame_main, data_input=self.data_input, classLogger=self.classLogger).execute()
            if not process:
                raise Exception('Pasta não localizada')

            process.click()
            frame_process = self.set_frame()
            frame_process.wait_for_timeout(5000)

            frame_progress = self.change_frame(frame_process, "Andamento")
            frame_progress.wait_for_timeout(2000)
            frame_list = frame_progress.child_frames[0]

            if ValidarAndamentosUseCase(page=self.page, frame=frame_list, data_input=self.data_input, classLogger=self.classLogger).execute():
                raise Exception("Expediente já cadastrado")

            self.create_expediente(frame_list)

        except Exception as e:
            self.classLogger.message(f"Erro ao executar AndamentoUseCase: {str(e)}")
            raise

    def set_frame(self) -> Frame:
        self.page.wait_for_selector('iframe')
        frames = self.page.query_selector_all('iframe')
        if frames:
            last_frame = frames[-1]
            frame_name = last_frame.get_attribute('name')
            frame_id = last_frame.get_attribute('id')
            return self.page.frame(name=frame_name) if frame_name else self.page.frame(id=frame_id)
        return None

    def change_frame(self, frame: Frame, tab: str) -> Frame:
        frame.wait_for_selector(f'button:has-text("{tab}")').click()
        frame.wait_for_timeout(2000)
        return self.set_frame()

    def create_expediente(self, frame_list: Frame):
        frame_list.wait_for_selector('button:has-text("NOVO")').click()
        frame_list.wait_for_timeout(1000)
        frame_create = self.set_frame()

        CriarExpedienteUseCase(page=self.page, frame=frame_create, data_input=self.data_input, classLogger=self.classLogger).execute()

        pasta = frame_create.wait_for_selector('[name=Processo]').input_value()

        frame_create.wait_for_selector('button:has-text("Providências")').click()
        frame_prov = frame_create.child_frames[0]
        frame_prov.wait_for_selector('button:has-text("NOVO")').click()
        frame_prov.wait_for_timeout(1000)
        frame_prov_details = self.set_frame()

        InserirDadosProvidenciaUseCase(page=self.page, frame=frame_prov_details, data_input=self.data_input, classLogger=self.classLogger).execute()

        return {
            "Pasta": pasta,
            "Processo": self.data_input.processo,
            "DataCadastro": datetime.now().strftime("%d/%m/%Y")
        }
