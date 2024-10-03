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
                response = FormularioGeralUseCase(
                    page=self.page,
                    classLogger=self.classLogger,
                    data_input=self.data_input,
                    robot=self.robot
                ).execute()

                form_value_response = FormularioValorUseCase(
                    page=self.page,
                    classLogger=self.classLogger,
                    data_input=self.data_input,
                    robot=self.robot,
                    iframe=response.get('iframe')
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
                    "Pasta": response.codigo,
                    "Processo": self.data_input.numero_do_processo,
                    "DataCadastro": response.data_cadastro
                }
            ]
            return data
        except Exception as e:
            self.classLogger.message(e.args[0])
            raise e
