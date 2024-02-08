

import time
from models.cliente.cliente import Cliente
from modules.logger.Logger import Logger
from modules.robotCore.__model__.RobotModel import RobotModel
from playwright.sync_api import Page, BrowserContext, sync_playwright
from robots.judLegalone.useCases.criarPasta.criarPastaUseCase import CriarPastaUseCase
from robots.judLegalone.useCases.inserirArquivos.inserirArquivosUseCase import InserirArquivosUseCase
from robots.judLegalone.useCases.login.login import LoginJudLegaloneUseCase
from robots.judLegalone.useCases.logout.logoutUseCase import LogoutUseCase
from robots.judLegalone.useCases.validarEFormatarEntrada.validarEFormatarEntradaUseCase import ValidarEFormatarEntradaUseCase
from robots.judLegalone.useCases.validarPasta.validarPastaUseCase import ValidarPastaJudUseCase
from robots.judLegalone.useCases.verificacaoEnvolvidos.verificacaoEnvolvidosUseCase import VerificacaoEnvolvidosUseCase


class judLegalone:
    def __init__(
        self,
        con_rd,
        classLogger: Logger,
        json_recebido:str,
        task_id:str,
        identifier_tenant:str,
        cliente:Cliente,
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
                cliente=self.cliente
            ).execute()
            response_data = []
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(ignore_https_errors=True)
                page = context.new_page()
                page.on("request", lambda response: response_data.append(response))
                page.goto('https://signon.thomsonreuters.com/?productId=L1LC&returnto=https%3a%2f%2fwww.nextlegalone.com.br%2fOnePass%2fLoginOnePass%2f&bhcp=1')
                page.set_default_timeout(6000000)
                time.sleep(8)      
                LoginJudLegaloneUseCase(
                    page=page,
                    username=data_input.username,
                    password=data_input.password,
                    classLogger=self.classLogger
                ).execute()
                try:
                    response = ValidarPastaJudUseCase(
                        page=page,
                        nome_envolvido=data_input.nome_envolvido,
                        processo=data_input.processo,
                        classLogger=self.classLogger,
                        context=context
                    ).execute()
                    if response.found:
                        InserirArquivosUseCase(
                            page=page,
                            arquivo_principal=data_input.arquivo_principal,
                            context=context,
                            pasta=response.pasta,
                            url_pasta=response.url_pasta,
                            classLogger=self.classLogger,
                            processo=data_input.processo
                        ).execute()
                        data.error = False
                        data.data_return = [
                            {
                                "Pasta":response.pasta,
                                "Protocolo":response.protocolo
                            }
                        ]
                        LogoutUseCase(
                            page=page,
                            classLogger=self.classLogger
                        ).execute()
                    else: 
                        data_input = VerificacaoEnvolvidosUseCase(
                            classLogger=self.classLogger,
                            data_input=data_input,
                            context=context
                        ).execute()
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
                                "Protocolo":response.protocolo
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
                "Protocolo":""
            }]
            data.data_return = data_error

        finally:
            return data

