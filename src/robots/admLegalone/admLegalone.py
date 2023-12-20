

import time
from models.cliente.cliente import Cliente
from modules.logger.Logger import Logger
from modules.robotCore.__model__.RobotModel import RobotModel
from playwright.sync_api import Page, BrowserContext, sync_playwright
from robots.admLegalone.useCases.criarPasta.criarPastaUseCase import CriarPastaUseCase
from robots.admLegalone.useCases.login.login import LoginAdmLegaloneUseCase
from robots.admLegalone.useCases.logout.logoutUseCase import LogoutUseCase
from robots.admLegalone.useCases.validarEFormatarEntrada.validarEFormatarEntradaUseCase import ValidarEFormatarEntradaUseCase
from robots.admLegalone.useCases.validarPasta.validarPastaUseCase import ValidarPastaUseCase


class AdmLegalone:
    def __init__(
        self,
        con_rd,
        classLogger: Logger,
        json_recebido:str,
        task_id:str,
        identifier_tenant:str,
        cliente:Cliente
    ) -> None:
        self.con_rd = con_rd
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.task_id = task_id
        self.identifier_tenant = identifier_tenant
        self.cliente = cliente

    def execute(self):
        data: RobotModel = RobotModel(
            error=True,
            data_return=[]
        )
        try:
            data_input = ValidarEFormatarEntradaUseCase(
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                cliente=self.cliente
            ).execute()
            response_data = []
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context(ignore_https_errors=True)
                page = context.new_page()
                page.on("request", lambda response: response_data.append(response))
                page.goto('https://signon.thomsonreuters.com/?productId=L1LC&returnto=https%3a%2f%2fwww.nextlegalone.com.br%2fOnePass%2fLoginOnePass%2f&bhcp=1')
                time.sleep(8)      
                LoginAdmLegaloneUseCase(
                    page=page,
                    username=data_input.username,
                    password=data_input.password,
                    classLogger=self.classLogger
                ).execute()
                try:
                    response = ValidarPastaUseCase(
                        page=page,
                        nome_envolvido=data_input.nome_envolvido,
                        numero_reclamacao=data_input.numero_reclamacao,
                        classLogger=self.classLogger
                    ).execute()
                    if response.found:
                        data.error = False
                        data.data_return = [
                            {
                                "Pasta":response.pasta,
                                "DataCadastro":response.data_cadastro
                            }
                        ]
                        LogoutUseCase(
                            page=page,
                            classLogger=self.classLogger
                        ).execute()
                    else:
                        response = CriarPastaUseCase(
                            page=page,
                            data_input=data_input,
                            classLogger=self.classLogger,
                            context=context
                        ).execute()
                        data.error = False
                        data.data_return = [
                            {
                                "Pasta":response.pasta,
                                "DataCadastro":response.data_cadastro
                            }
                        ]
                        LogoutUseCase(
                            page=page,
                            classLogger=self.classLogger
                        ).execute()
                except Exception as error:
                    LogoutUseCase(
                        page=page,
                        classLogger=self.classLogger
                    ).execute()
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

