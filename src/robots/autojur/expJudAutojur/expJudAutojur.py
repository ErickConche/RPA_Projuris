import json
import time
from datetime import datetime
from modules.logger.Logger import Logger
from modules.excecoes.excecao import ExcecaoGeral
from models.cookies.cookiesUseCase import CookiesUseCase
from modules.robotCore.__model__.RobotModel import RobotModel
from models.cliente.__model__.ClienteModel import ClienteModel
from global_variables.login_exp_autojur import get_execution_login, update_execution_login
from robots.autojur.expJudAutojur.useCases.novoLogin.novoLoginUseCase import NovoLoginUseCase
from robots.autojur.expJudAutojur.useCases.buscarPessoa.buscarPessoaUseCase import BuscarPessoaUseCase
from robots.autojur.expJudAutojur.useCases.validarCookies.validarCookiesUseCase import ValidarCookiesUseCase
from robots.autojur.expJudAutojur.useCases.validarEFormatarEntrada.validarEFormatarEntradaUseCase import ValidarEFormatarEntradaUseCase
from robots.autojur.expJudAutojur.useCases.iniciandoProcessoExpAutojur.iniciandoProcessoExpAutojurUseCase import IniciandoProcessoExpAutojurUseCase


class ExpJudAutojur:
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
        self.queue = 'app-exp-jud-autojur'

    def execute(self):
        data: RobotModel = RobotModel(
            error=True,
            data_return=[]
        )
        message = f"Inicio da aplicação {str(datetime.now())} da tarefa {json.loads(self.json_recebido)['TaskId']}"
        self.classLogger.message(message=message)
        try:
            data_input = ValidarEFormatarEntradaUseCase(
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                cliente=self.cliente,
                con_rd=self.con_rd,
                queue=self.queue
            ).execute()
            if data_input.cookie_session:
                cookies_validados = ValidarCookiesUseCase(data_input.cookie_session).execute()
                if not cookies_validados:
                    data_input.cookie_session = self.__obter_novo_cookie(
                        data_input,
                        self.classLogger,
                        self.cliente.id
                    )
            else:
                data_input.cookie_session = self.__obter_novo_cookie(
                    data_input,
                    self.classLogger,
                    self.cliente.id
                )
            try:
                data_input.id_responsavel = BuscarPessoaUseCase(
                    classLogger=self.classLogger,
                    cookies=data_input.cookie_session,
                    nome=data_input.responsavel
                ).execute()
                if not data_input.id_responsavel:
                    raise ExcecaoGeral("Não foi possivel encontrar o responsavel", "Responsável inválido")
                response = IniciandoProcessoExpAutojurUseCase(
                    data_input=data_input,
                    classLogger=self.classLogger,
                    cookies=data_input.cookie_session
                ).execute()
                data.error = True if 'Indício de tarefa já cadastrada' in response.codigo else False
                data.data_return = [
                    {
                        "Protocolo": response.codigo,
                        "DataCadastro": response.data_cadastro
                    }
                ]
            except ExcecaoGeral as error:
                raise error
            except Exception as error:
                raise ExcecaoGeral(str(error))
        except ExcecaoGeral as error:
            message = f"Erro: {error.log_erro}"
            self.classLogger.message(message)
            data_error = [{
                "Protocolo": error.msg_erro
            }]
            data.data_return = data_error
        finally:
            return data

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
