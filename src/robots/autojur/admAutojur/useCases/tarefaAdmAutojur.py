
import time
from modules.logger.Logger import Logger
from playwright.sync_api import sync_playwright
from modules.robotCore.__model__.RobotModel import RobotModel
from models.cliente.__model__.ClienteModel import ClienteModel
from robots.autojur.useCases.login.login import LoginAutojurUseCase
from robots.autojur.admAutojur.useCases.criarCodigo.criarCodigoUseCase import CriarCodigoUseCase
from robots.autojur.admAutojur.useCases.validarPastaAutojur.validarPastaAutojurUseCase import ValidarPastaAutojurUseCase
from robots.autojur.admAutojur.useCases.verificacaoEnvolvidos.verificacaoEnvolvidosUseCase import VerificacaoEnvolvidosAdmUseCase
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.validarEFormatarEntradaTarefaUseCase import (
    ValidarEFormatarEntradaTarefaUseCase)
from robots.autojur.admAutojur.useCases.validarPastaAutojur.validarPastaAutojurTarefaUseCase import (
    ValidarPastaAutojurTarefaUseCase)
from robots.autojur.admAutojur.inserirTarefa.inserirTarefaUseCase import InserirTarefaUseCase

class TarefaAdmAutoJur:
    def __init__(
        self,
        con_rd,
        classLogger: Logger,
        json_recebido:str,
        task_id:str,
        identifier_tenant:str,
        cliente:ClienteModel,
        id_queue: int
    ) -> None:
        self.con_rd = con_rd
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.task_id = task_id
        self.identifier_tenant = identifier_tenant
        self.cliente = cliente
        self.id_queue = id_queue

    def execute(self):
        data: RobotModel = RobotModel(
            error=True,
            data_return=[]
        )
        try:
            data_input = ValidarEFormatarEntradaTarefaUseCase(
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                cliente=self.cliente,
                con_rd=self.con_rd
            ).execute()
            response_data = []
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(ignore_https_errors=True)
                page = context.new_page()
                context.add_cookies([{"name":"footprint", "value": data_input.footprint, "url": data_input.url_cookie}])
                page.on("request", lambda response: response_data.append(response))
                page.set_default_timeout(300000)
                page.goto('https://baz.autojur.com.br/login.jsf')
                time.sleep(8)      
                LoginAutojurUseCase(
                    page=page,
                    username=data_input.username,
                    password=data_input.password,
                    classLogger=self.classLogger
                ).execute()
                try:
                    response = ValidarPastaAutojurTarefaUseCase(
                        page=page,
                        pasta=data_input.dados_busca,
                        classLogger=self.classLogger
                    ).execute()
                    if response:
                        InserirTarefaUseCase(
                            page=page,
                            data_input=data_input,
                            localizador=data_input.dados_busca,
                            classLogger=self.classLogger
                        ).execute()
                        data.error = False
                        data.data_return = [
                            {
                                "Protocolo":response.get('codigo'),
                                "DataCadastro":data_input.data
                            }
                        ]
                except Exception as error:
                    raise error
                browser.close()

        except Exception as error:
            message = f"Erro: {error}"
            self.classLogger.message(message)
            data_error = [{
                "Protocolo":"SITE INDISPONÍVEL",
                "DataCadastro":""
            }]
            data.data_return = data_error

        finally:
            return data