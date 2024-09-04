import time
from modules.logger.Logger import Logger
from playwright.sync_api import BrowserContext, Page
from modules.robotCore.__model__.RobotModel import RobotModel
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from robots.espaider.useCases.formularioAndamentos.formularioAndamentosUseCase import FormularioAndamentosUseCase
from robots.espaider.useCases.formularioGeral.formularioGeralUseCase import (
    FormularioGeralUseCase)
from robots.espaider.useCases.formularioArquivos.formularioArquivosUseCase import FormularioArquivosUseCase
from robots.espaider.useCases.formularioGpaAreas.formularioGpaAreasUseCase import FormularioGpaAreasUseCase
from robots.espaider.useCases.formularioValor.formularioValorUseCase import FormularioValorUseCase
from robots.espaider.useCases.paginaProcessos.paginaProcessosUseCase import PaginaProcessosUseCase
from robots.espaider.useCases.validarPastaEspaider.validarPastaEspaiderUseCase import ValidarPastaEspaiderUseCase


class criarCodigoCadastroUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderModel,
        classLogger: Logger,
        context: BrowserContext,
        robot: str,
        system_url: str
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.context = context
        self.robot = robot
        self.system_url = system_url

    def execute(self):
        try:
            inicio = time.time()
            data: RobotModel = RobotModel(
                error=True,
                data_return=[]
            )
            if '#processos/processos' not in self.page.url:
                PaginaProcessosUseCase(
                    page=self.page,
                    classLogger=self.classLogger,
                    data_input=self.data_input,
                    robot=self.robot,
                    system_url=self.system_url
                ).execute()
            response = ValidarPastaEspaiderUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger
            ).execute(attempt=1)
            if not response.found:
                iframe = response.iframe
                button = iframe.query_selector('[data-icon="add_circle"]')
                button.click()
                self.page.wait_for_load_state('load')

                self.page.wait_for_selector('iframe')
                frames = self.page.query_selector_all('iframe')
                if frames:
                    last_frame = frames[-1]

                    frame_name = last_frame.get_attribute('name')
                    frame_id = last_frame.get_attribute('id')

                    if frame_name or frame_id:
                        iframe = self.page.frame(name=frame_name) if frame_name else self.page.frame(id=frame_id)
                        iframe.wait_for_load_state("load")

                FormularioGeralUseCase(
                    page=self.page,
                    classLogger=self.classLogger,
                    data_input=self.data_input,
                    robot=self.robot,
                    iframe=iframe
                ).execute()

                form_value_response = FormularioValorUseCase(
                    page=self.page,
                    classLogger=self.classLogger,
                    data_input=self.data_input,
                    robot=self.robot,
                    iframe=iframe
                ).execute()

                files_response = FormularioArquivosUseCase(
                    page=self.page,
                    classLogger=self.classLogger,
                    data_input=self.data_input,
                    robot=self.robot,
                    iframe=form_value_response.get('iframe')
                ).execute()

                form_gpa_response = FormularioGpaAreasUseCase(
                    page=self.page,
                    classLogger=self.classLogger,
                    data_input=self.data_input,
                    robot=self.robot,
                    iframe=files_response.get('iframe')
                ).execute()

                FormularioAndamentosUseCase(
                    page=self.page,
                    classLogger=self.classLogger,
                    data_input=self.data_input,
                    robot=self.robot,
                    iframe=form_gpa_response.get('iframe')
                ).execute()

                PaginaProcessosUseCase(
                    page=self.page,
                    classLogger=self.classLogger,
                    data_input=self.data_input,
                    robot=self.robot,
                    system_url=self.system_url
                ).execute()
                response = ValidarPastaEspaiderUseCase(
                    page=self.page,
                    data_input=self.data_input,
                    classLogger=self.classLogger
                ).execute(attempt=2)
            fim = time.time()
            tempo_execucao = fim - inicio
            print(f"Tempo de execução: {tempo_execucao} segundos")
            data.error = False
            data.data_return = [
                {
                    "Protocolo": response.codigo,
                    "DataCadastro": response.data_cadastro
                }
            ]
            return data
        except Exception as e:
            self.classLogger.message(e.args[0])
            raise e
