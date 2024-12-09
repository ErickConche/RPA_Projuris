import os
import json
import time
from models.cliente.__model__.ClienteModel import ClienteModel
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from multiprocessing import Manager, Process
from playwright.sync_api import sync_playwright
from models.cookies.cookiesUseCase import CookiesUseCase
from database.Postgres import create_connect as create_con_pg
from modules.robotCore.__model__.RobotModel import RobotModel, RobotModelParalel
from global_variables.login_exp_autojur import get_execution_login, update_execution_login
from robots.autojur.admAutojur.useCases.novoLogin.novoLoginUseCase import NovoLoginUseCase
from robots.autojur.admAutojur.useCases.criarCodigo.criarCodigoUseCase import CriarCodigoUseCase
from robots.autojur.admAutojur.useCases.validarCookies.validarCookiesUseCase import ValidarCookiesUseCase
from robots.autojur.admAutojur.useCases.validarPastaAutojur.validarPastaAutojurUseCase import ValidarPastaAutojurUseCase
from robots.autojur.admAutojur.useCases.verificacaoEnvolvidos.verificacaoEnvolvidosUseCase import VerificacaoEnvolvidosAdmUseCase
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.validarEFormatarEntradaUseCase import ValidarEFormatarEntradaUseCase


class AdmAutoJur:
    def __init__(
        self,
        con_rd,
        classLogger: Logger,
        json_recebido: str,
        task_id: str,
        identifier_tenant: str,
        cliente: ClienteModel,
        id_queue: int
    ) -> None:
        self.con_rd = con_rd
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.task_id = task_id
        self.identifier_tenant = identifier_tenant
        self.cliente = cliente
        self.id_queue = id_queue
        self.queue = 'app-adm-autojur'
        self.results = []

    # def threadPoolExecute(self):
    #     list_process = []
    #     manager = Manager()
    #     self.results = manager.list()
    #     for requisicao in self.requisicoes:
    #         process = Process(target=self.execute, args=(requisicao,))
    #         process.start()
    #         list_process.append(process)
    #         time.sleep(3)
    #     for process in list_process:
    #         process.join()
    #     return self.results

    def execute(self):
        data: RobotModel = RobotModel(
            error=True,
            data_return=[]
        )
        data_input = ValidarEFormatarEntradaUseCase(
            classLogger=self.classLogger,
            json_recebido=self.json_recebido,
            cliente=self.cliente,
            con_rd=self.con_rd
        ).execute()
        response_data = []
        session_cookies = ''
        if data_input.cookie_session:
            session_cookies = data_input.cookie_session
            cookies_validados = ValidarCookiesUseCase(data_input.cookie_session).execute()
            if not cookies_validados:
                session_cookies = self.__obter_novo_cookie(
                    data_input,
                    self.classLogger,
                    self.cliente.id,
                )
        else:
            session_cookies = self.__obter_novo_cookie(
                data_input,
                self.classLogger,
                self.cliente.id,
            )
        try:
            session_cookies = json.loads(session_cookies)
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(ignore_https_errors=True)
                page = context.new_page()
                context.add_cookies(session_cookies)
                page.on("request", lambda response: response_data.append(response))
                page.set_default_timeout(300000)
                try:
                    response = ValidarPastaAutojurUseCase(
                        page=page,
                        pasta=data_input.pasta,
                        numero_reclamacao=data_input.numero_reclamacao,
                        classLogger=self.classLogger
                    ).execute()
                    if response.found:
                        data.error = False
                        data.data_return = [
                            {
                                "Protocolo": response.codigo,
                                "DataCadastro": response.data_cadastro
                            }
                        ]
                    else:
                        data_input = VerificacaoEnvolvidosAdmUseCase(
                            classLogger=self.classLogger,
                            data_input=data_input,
                            context=context
                        ).execute()
                        response = CriarCodigoUseCase(
                            page=page,
                            data_input=data_input,
                            classLogger=self.classLogger,
                            context=context
                        ).execute()
                        data.error = False
                        data.data_return = [
                            {
                                "Protocolo": response.codigo,
                                "DataCadastro": response.data_cadastro
                            }
                        ]
                except Exception as error:
                    raise error
                browser.close()

        except Exception as error:
            message = f"Erro: {error}"
            self.classLogger.message(message)
            data_error = [{
                "Protocolo": "SITE INDISPONÍVEL",
                "DataCadastro": ""
            }]
            data.data_return = data_error
        finally:
            return data

    def __obter_novo_cookie(self, data_input, classLogger, cliente_id):
        if get_execution_login():
            while get_execution_login():
                time.sleep(3)
                print('Aguardando a execução anterior finalizar o login')
            return CookiesUseCase(con_rd=self.con_rd).buscarCookies(
                idcliente=cliente_id,
                queue=self.queue
            ).session_cookie

        update_execution_login(True)

        session_cookie = NovoLoginUseCase(
            classLogger=classLogger,
            queue=self.queue,
            data_input=data_input,
            con_rd=self.con_rd,
            idcliente=cliente_id
        ).execute()

        update_execution_login(False)
        return session_cookie
