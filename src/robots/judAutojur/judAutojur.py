
import time

from bs4 import BeautifulSoup
from models.cliente.__model__.ClienteModel import ClienteModel
from models.cliente.cliente import Cliente
from modules.logger.Logger import Logger
from modules.robotCore.__model__.RobotModel import RobotModel
from playwright.sync_api import Page, BrowserContext, sync_playwright
from robots.judAutojur.useCases.criarCodigo.criarCodigoUseCase import CriarCodigoUseCase
from robots.judAutojur.useCases.login.login import LoginJudAutojurUseCase

from robots.judAutojur.useCases.validarEFormatarEntrada.validarEFormatarEntradaUseCase import ValidarEFormatarEntradaUseCase
from robots.judAutojur.useCases.validarPastaAutojur.validarPastaAutojurUseCase import ValidarPastaAutojurUseCase


class JudAutojur:
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
            data_input = ValidarEFormatarEntradaUseCase(
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
                LoginJudAutojurUseCase(
                    page=page,
                    username=data_input.username,
                    password=data_input.password,
                    classLogger=self.classLogger
                ).execute()
                try:
                    response = ValidarPastaAutojurUseCase(
                        page=page,
                        pasta=data_input.pasta,
                        processo=data_input.processo,
                        classLogger=self.classLogger
                    ).execute()
                    if response.found:
                        data.error = False
                        data.data_return = [
                            {
                                "Protocolo":response.codigo
                            }
                        ]
                    else:
                        response = CriarCodigoUseCase(
                            page=page,
                            data_input=data_input,
                            classLogger=self.classLogger,
                            context=context
                        ).execute()
                        data.error = False
                        data.data_return = [
                            {
                                "Protocolo":response.codigo
                            }
                        ]
                except Exception as error:
                    raise error
                browser.close()

        except Exception as error:
            message = f"Erro: {error}"
            self.classLogger.message(message)
            data_error = [{
                "Pasta":"SITE INDISPONÍVEL",
                "DataCadastro":""
            }]
            data.data_return = data_error

        finally:
            return data