import time
from modules.logger.Logger import Logger
from playwright.sync_api import sync_playwright
from modules.robotCore.__model__.RobotModel import RobotModel
from models.cliente.__model__.ClienteModel import ClienteModel
from robots.autojur.useCases.login.login import LoginAutojurUseCase
from robots.autojur.identExpJudAutojur.useCases.validarEFormatarEntrada.validarEFormatarEntradaUseCase import ValidarEFormatarEntradaUseCase
from robots.autojur.identExpJudAutojur.useCases.procurarProcessoAutojur.procurarProcessoAutojurUseCase import ProcurarProcessoAutojurUseCase

class IdentExpJudAutojur:

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
                LoginAutojurUseCase(
                    page=page,
                    username=data_input.username,
                    password=data_input.password,
                    classLogger=self.classLogger
                ).execute()
                try:
                    response = ProcurarProcessoAutojurUseCase(
                        page=page,
                        processo=data_input.processo,
                        data_expediente=data_input.data_expediente,
                        tipo_expediente=data_input.tipo_expediente,
                        classLogger=self.classLogger,
                        context=context
                    ).execute()
                    data.error = False
                    data.data_return = [{
                        "Processo":data_input.processo,
                        "ProcessoCadastrado":response.processo_cadastrado,
                        "DataExpediente":response.data_expediente,
                        }]
                except Exception as error:
                    raise error
                browser.close()

        except Exception as error:
            message = f"Erro: {error}"
            self.classLogger.message(message)
            data_error = [{
                "Número do processo":data_input.processo,
                "ProcessoCadastrado": '',
                "DataExpediente": '',
            }]
            data.data_return = data_error

        finally:
            return data