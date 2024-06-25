import time
from modules.logger.Logger import Logger
from playwright.sync_api import sync_playwright
from models.cliente.cliente import Cliente
from modules.robotCore.__model__.RobotModel import RobotModel
from robots.legalone.useCases.login.login import LoginLegaloneUseCase
from robots.legalone.judLegalone.useCases.criarPasta.criarPastaUseCase import CriarPastaUseCase
from robots.legalone.judLegalone.useCases.validarPasta.validarPastaUseCase import ValidarPastaJudUseCase
from robots.legalone.judLegalone.useCases.inserirArquivos.inserirArquivosUseCase import InserirArquivosUseCase
from robots.legalone.judLegalone.useCases.verificacaoEnvolvidos.verificacaoEnvolvidosUseCase import VerificacaoEnvolvidosUseCase
from robots.legalone.judLegalone.useCases.validarEFormatarEntrada.validarEFormatarEntradaUseCase import ValidarEFormatarEntradaUseCase


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
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context(ignore_https_errors=True)
                page = context.new_page()
                page.on("request", lambda response: response_data.append(response))
                page.goto('https://signon.thomsonreuters.com/?productId=L1LC&returnto=https%3a%2f%2fwww.nextlegalone.com.br%2fOnePass%2fLoginOnePass%2f&bhcp=1')
                page.set_default_timeout(600000)
                time.sleep(8)      
                LoginLegaloneUseCase(
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
                        processo_originario=data_input.processo_originario,
                        classLogger=self.classLogger,
                        context=context
                    ).execute()
                    if response.found:
                        InserirArquivosUseCase(
                            arquivo_principal=data_input.arquivo_principal,
                            context=context,
                            url_pasta=response.url_pasta,
                            classLogger=self.classLogger,
                            processo=data_input.processo
                        ).execute()
                        data.error = False
                        data.data_return = [
                            {
                                "Pasta":response.pasta,
                                "Protocolo":response.protocolo,
                                "DataCadastro":response.data_cadastro
                            }
                        ]
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
                            context=context,
                            url_pasta_originaria=response.url_pasta_originaria
                        ).execute()
                        data.error = False
                        data.data_return = [
                            {
                                "Pasta":response.pasta,
                                "Protocolo":response.protocolo,
                                "DataCadastro":response.data_cadastro
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
                "Protocolo":"",
                "DataCadastro":""
            }]
            data.data_return = data_error

        finally:
            return data
