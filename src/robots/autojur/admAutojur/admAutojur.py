import os
import json
import time
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from multiprocessing import Manager, Process
from playwright.sync_api import sync_playwright
from models.cookies.cookiesUseCase import CookiesUseCase
from database.Postgres import create_connect as create_con_pg
from modules.robotCore.__model__.RobotModel import RobotModelParalel
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
        requisicoes: list
    ) -> None:
        # self.con_rd = con_rd
        # self.class_cliente = Cliente(con=con_rd)
        self.requisicoes = requisicoes
        self.queue = 'app-adm-autojur'

    def threadPoolExecute(self):
        list_process = []
        manager = Manager()
        self.results = manager.list()
        for requisicao in self.requisicoes:
            process = Process(target=self.execute, args=(requisicao,))
            process.start()
            list_process.append(process)
            time.sleep(3)
        for process in list_process:
            process.join()
        return self.results

    def execute(self, execucao):
        con_rd = create_con_pg(
            host=os.getenv("HOSTRD"),
            port=os.getenv("PORTRD"),
            database=os.getenv("DBRD"),
            user=os.getenv("USERRD"),
            password=os.getenv("PASSRD")
        ).get_connect()
        class_cliente = Cliente(con=con_rd)
        json_recebido = execucao.get('json_recebido')
        json_obj = json.loads(json_recebido)
        classLogger = Logger(hiring_id=json_obj.get('TaskId'))
        cliente = class_cliente.buscarCliente(tenant=json_obj.get('IdentifierTentant'))
        data: RobotModelParalel = RobotModelParalel(
            error=True,
            data_return=[],
            identifier_tenant=json_obj.get('IdentifierTentant'),
            classLogger=classLogger,
            task_id=json_obj.get('TaskId'),
            id_requisicao=execucao.get('id'),
            json_recebido=json_obj
        )
        data_input = ValidarEFormatarEntradaUseCase(
            classLogger=classLogger,
            json_recebido=json_recebido,
            cliente=cliente,
            con_rd=con_rd
        ).execute()
        response_data = []
        session_cookies = ''
        if data_input.cookie_session:
            session_cookies = data_input.cookie_session
            cookies_validados = ValidarCookiesUseCase(data_input.cookie_session).execute()
            if not cookies_validados:
                session_cookies = self.__obter_novo_cookie(
                    data_input,
                    classLogger,
                    cliente.id,
                    con_rd
                )
        else:
            session_cookies = self.__obter_novo_cookie(
                data_input,
                classLogger,
                cliente.id,
                con_rd
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
                        classLogger=classLogger
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
                            classLogger=classLogger,
                            data_input=data_input,
                            context=context
                        ).execute()
                        response = CriarCodigoUseCase(
                            page=page,
                            data_input=data_input,
                            classLogger=classLogger,
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
            classLogger.message(message)
            data_error = [{
                "Protocolo": "SITE INDISPONÍVEL",
                "DataCadastro": ""
            }]
            data.data_return = data_error

        finally:
            con_rd.close()
            self.results.append(data)

    def __obter_novo_cookie(self, data_input, classLogger, cliente_id, con_rd):
        if get_execution_login():
            while get_execution_login():
                time.sleep(3)
                print('Aguardando a execução anterior finalizar o login')
            return CookiesUseCase(con_rd=con_rd).buscarCookies(
                idcliente=cliente_id,
                queue=self.queue
            ).session_cookie

        update_execution_login(True)

        session_cookie = NovoLoginUseCase(
            classLogger=classLogger,
            queue=self.queue,
            data_input=data_input,
            con_rd=con_rd,
            idcliente=cliente_id
        ).execute()

        update_execution_login(False)
        return session_cookie
