import json
import time
from modules.logger.Logger import Logger
from playwright.sync_api import sync_playwright
from modules.excecoes.excecao import ExcecaoGeral
from models.cookies.cookiesUseCase import CookiesUseCase
from robots.autojur.useCases.login.login import LoginAutojurUseCase
from robots.autojur.expJudAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class NovoLoginUseCase:
    def __init__(
        self,
        classLogger: Logger,
        queue: str,
        data_input: DadosEntradaFormatadosModel,
        con_rd,
        idcliente
    ) -> None:
        self.classLogger = classLogger
        self.data_input = data_input
        self.queue = queue
        self.con_rd = con_rd
        self.idcliente = idcliente

    def execute(self):
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context(ignore_https_errors=True)
                page = context.new_page()
                context.add_cookies([
                    {
                        "name": "footprint",
                        "value": self.data_input.footprint,
                        "url": self.data_input.url_cookie
                    }
                ])
                page.set_default_timeout(300000)
                page.goto('https://baz.autojur.com.br/login.jsf')
                time.sleep(8)      
                LoginAutojurUseCase(
                    page=page,
                    username=self.data_input.username,
                    password=self.data_input.password,
                    classLogger=self.classLogger
                ).execute()
                cookies = context.cookies()
                cookie_session_dict = []
                for cookie in cookies:
                    cookie_session_dict.append({
                        'name': cookie.get('name'),
                        'value': cookie.get('value'),
                        'domain': cookie.get('domain'),
                        'path': cookie.get('path'),
                        'secure': cookie.get('secure')
                    })
                cookie_session = json.dumps(cookie_session_dict)

                CookiesUseCase(
                    con_rd=self.con_rd
                ).alterarCookieSession(
                    queue=self.queue,
                    cookie_session=cookie_session,
                    idcliente=self.idcliente
                )
                page.close()
                return cookie_session
        except Exception as error:
            error_excecao_geral = ExcecaoGeral(str(error), "Erro ao realizar login")
            message = "Erro ao realizar novo login"
            self.classLogger.message(message)
            raise error_excecao_geral
