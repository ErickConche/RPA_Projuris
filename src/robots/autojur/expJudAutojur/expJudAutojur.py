import json
import time
from threading import Thread
from datetime import datetime
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from modules.excecoes.excecao import ExcecaoGeral
from models.cookies.cookiesUseCase import CookiesUseCase
from modules.robotCore.__model__.RobotModel import RobotModelParalel
from global_variables.login_exp_autojur import get_execution_login, update_execution_login
from robots.autojur.expJudAutojur.useCases.novoLogin.novoLoginUseCase import NovoLoginUseCase
from robots.autojur.expJudAutojur.useCases.buscarPessoa.buscarPessoaUseCase import BuscarPessoaUseCase
from robots.autojur.expJudAutojur.useCases.validarCookies.validarCookiesUseCase import ValidarCookiesUseCase
from robots.autojur.expJudAutojur.useCases.validarEFormatarEntrada.validarEFormatarEntradaUseCase import ValidarEFormatarEntradaUseCase
from robots.autojur.expJudAutojur.useCases.iniciandoProcessoExpAutojur.iniciandoProcessoExpAutojurUseCase import IniciandoProcessoExpAutojurUseCase


class ExpJudAutojur:
    def __init__(
        self,
        queue,
        con_rd,
        requisicoes: dict,
    ) -> None:
        self.con_rd = con_rd
        self.requisicoes = requisicoes
        self.queue = queue
        self.class_cliente = Cliente(con=con_rd)
        self.results = []

    def thread(self, requisicao):
        json_recebido = json.loads(requisicao['json_recebido'])
        classLogger = Logger(hiring_id=json_recebido['TaskId'])
        data: RobotModelParalel = RobotModelParalel(
            error=True,
            data_return=[],
            classLogger=classLogger,
            identifier_tenant=json_recebido['IdentifierTentant'],
            task_id=json_recebido['TaskId'],
            id_requisicao=requisicao.get("id"),
            json_recebido=json_recebido
        )
        message = f"Inicio da aplicação {str(datetime.now())} da tarefa {json_recebido['TaskId']}"
        classLogger.message(message=message)
        cliente = self.class_cliente.buscarCliente(tenant=json_recebido['IdentifierTentant'])
        try:
            data_input = ValidarEFormatarEntradaUseCase(
                classLogger=classLogger,
                json_recebido=json_recebido,
                cliente=cliente,
                con_rd=self.con_rd,
                queue=self.queue
            ).execute()
            if data_input.cookie_session:
                cookies_validados = ValidarCookiesUseCase(data_input.cookie_session).execute()
                if not cookies_validados:
                    data_input.cookie_session = self.__obter_novo_cookie(
                        data_input, 
                        classLogger,
                        cliente.id
                    )
            else:
                data_input.cookie_session = self.__obter_novo_cookie(
                    data_input, 
                    classLogger,
                    cliente.id
                )
            try:
                data_input.id_responsavel = BuscarPessoaUseCase(
                    classLogger=classLogger,
                    cookies=data_input.cookie_session,
                    nome=data_input.responsavel
                ).execute()
                if not data_input.id_responsavel:
                    raise ExcecaoGeral("Não foi possivel encontrar o responsavel","Responsável inválido")
                response = IniciandoProcessoExpAutojurUseCase(
                    data_input=data_input,
                    classLogger=classLogger,
                    cookies=data_input.cookie_session
                ).execute()
                data.error = False
                data.data_return = [
                    {
                        "Protocolo":response.codigo
                    }
                ]
            except ExcecaoGeral as error:
                raise error
            except Exception as error:
                raise ExcecaoGeral(str(error))
        except ExcecaoGeral as error:
            message = f"Erro: {error.log_erro}"
            classLogger.message(message)
            data_error = [{
                "Protocolo":error.msg_erro
            }]
            data.data_return = data_error
        finally:
            self.results.append(data)

    def execute(self):
        list_threads = []
        for requisicao in self.requisicoes:
            thread = Thread(target=self.thread, args=(
                    requisicao,
                )
            )
            thread.start()
            list_threads.append(thread)
            time.sleep(3)
        for thread in list_threads:
            thread.join()
        return self.results
        
    def __obter_novo_cookie(self, data_input, classLogger, cliente_id):
        if get_execution_login():
            while get_execution_login():
                time.sleep(3)
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