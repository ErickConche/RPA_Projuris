
import json
import time
from modules.logger.Logger import Logger
from playwright.sync_api import sync_playwright
from models.cookies.cookiesUseCase import CookiesUseCase
from modules.robotCore.__model__.RobotModel import RobotModel
from models.cliente.__model__.ClienteModel import ClienteModel
from global_variables.login_tarefa_adm_autojur import get_execution_login, update_execution_login
from robots.autojur.admAutojur.useCases.novoLogin.novoLoginUseCase import NovoLoginUseCase
from robots.autojur.admAutojur.useCases.validarCookies.validarCookiesUseCase import ValidarCookiesUseCase
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
            session_cookies = ''
            if data_input.cookie_session:
                session_cookies = data_input.cookie_session
                cookies_validados = ValidarCookiesUseCase(data_input.cookie_session).execute()
                if not cookies_validados:
                    session_cookies = self.__obter_novo_cookie(
                        data_input,
                        self.classLogger,
                        self.cliente.id
                    )
            else:
                session_cookies = self.__obter_novo_cookie(
                    data_input,
                    self.classLogger,
                    self.cliente.id
                )
            session_cookies = json.loads(session_cookies)
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(ignore_https_errors=True)
                page = context.new_page()
                context.add_cookies(session_cookies)
                page.on("request", lambda response: response_data.append(response))
                page.set_default_timeout(300000)
                try:
                    response = ValidarPastaAutojurTarefaUseCase(
                        page=page,
                        pasta=data_input.dados_busca,
                        classLogger=self.classLogger
                    ).execute()
                    if response:
                        data.error = InserirTarefaUseCase(
                            page=page,
                            data_input=data_input,
                            localizador=data_input.dados_busca,
                            classLogger=self.classLogger
                        ).execute()
                        if not data.error:
                            data.data_return = [
                                {
                                    "Protocolo": response.get('codigo'),
                                    "DataCadastro": data_input.data
                                }
                            ]
                        else:
                            data.data_return = [
                                {
                                    "Protocolo": "Erro ao cadastrar a tarefa",
                                    "DataCadastro": ""
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
