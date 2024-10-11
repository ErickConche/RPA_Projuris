import requests
from modules.logger.Logger import Logger
from playwright.sync_api import sync_playwright
from models.cookies.cookiesUseCase import CookiesUseCase
from models.cliente.__model__.ClienteModel import ClienteModel
from robots.espaider.useCases.login.loginEspaiderUseCase import LoginEspaiderUseCase
from robots.espaider.useCases.criarCodigo.criarCodigoUseCase import CriarCodigoUseCase
from robots.espaider.useCases.criarCodigo.criarCodigoExpUseCase import CriarCodigoExpUseCase
from robots.espaider.useCases.criarCodigo.criarCodigoCadastroUseCase import criarCodigoCadastroUseCase
from robots.espaider.useCases.checkSystemStatus.checkSystemStatusUseCase import CheckSystemStatusUseCase
from robots.espaider.useCases.validarEFormatarEntrada.validarEFormatarEntradaUseCase import ValidarEFormatarEntradaUseCase
from robots.espaider.useCases.login.loginMicrosoftUseCase import LoginMicrosoftUseCase


class InitRegisterUseCase:
    def __init__(
        self,
        con_rd,
        classLogger: Logger,
        json_recebido: str,
        task_id: str,
        identifier_tenant: str,
        queue: str,
        client: ClienteModel,
        robot: str
    ) -> None:
        self.con_rd = con_rd
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.task_id = task_id
        self.identifier_tenant = identifier_tenant
        self.queue = queue
        self.client = client
        self.robot = robot

    def execute(self):
        tenant_domain = self.identifier_tenant.split('.')[0]

        queue_organization = f"app-espaider-{tenant_domain}"
        try:
            data_input = ValidarEFormatarEntradaUseCase(
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                client=self.client,
                con_rd=self.con_rd,
                robot=self.robot,
                queue=queue_organization
            ).execute()
            response_data = []
            system_url = self.client.base_url
            session = requests.Session()
            if data_input.cookie_session:
                cookie = requests.cookies.create_cookie(
                    name="cookie", value=data_input.cookie_session)
                session.cookies.set_cookie(cookie)
                cookies = session.cookies.get_dict()
                domain = system_url.split('//')[1].split('/')[0]
                playwright_cookies = self.parse_cookie_string(
                    cookie_string=data_input.cookie_session, domain=domain)

            status_response = CheckSystemStatusUseCase(
                system_url=system_url,
                session=session,
                classLogger=self.classLogger
            ).execute()
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(ignore_https_errors=True)
                if data_input.cookie_session:
                    context.add_cookies(playwright_cookies)
                page = context.new_page()
                page.on("request", lambda response: response_data.append(response))
                page.set_default_timeout(30000)
                page.goto(system_url,
                          wait_until='load')
                if not status_response.get('success') or not data_input.cookie_session or '/login/' in page.url:
                    status_response = LoginEspaiderUseCase(
                        page=page,
                        username=data_input.username,
                        password=data_input.password,
                        classLogger=self.classLogger
                    ).execute() if not 'login.microsoftonline.com' in page.url else LoginMicrosoftUseCase(
                        page=page, 
                        classLogger=self.classLogger, 
                        user=data_input.username,
                        password=data_input.password
                    ).execute()
                    if not status_response.get('success'):
                        raise ("Site indisponivel")
                    cookies = context.cookies()
                    cookie_session = ""
                    for cookie in cookies:
                        cookie_session += f'{cookie.get("name")}={cookie.get("value")};'
                    CookiesUseCase(
                        con_rd=self.con_rd
                    ).alterarCookieSession(
                        idcliente=self.client.id,
                        queue=queue_organization,
                        cookie_session=cookie_session
                    )
                    
                if page.get_by_text("Vídeo de boas vindas").is_visible():
                    page.locator("button[data-icon='close']").click()
                if not page.query_selector('#userOptionsBtn'):
                    raise Exception('Credencial incorreta')
                if page.locator('[data-icon="close"]').is_visible():
                    page.query_selector('[data-icon="close"]').click()
                if page.locator('tour-popup > tour-popup-actions > button').is_visible():
                    page.query_selector('tour-popup > tour-popup-actions > button').click()
                    
                if self.robot == 'Cadastro':
                    return criarCodigoCadastroUseCase(
                        page=page,
                        data_input=data_input,
                        classLogger=self.classLogger,
                        context=context,
                        robot=self.robot,
                        system_url=system_url
                    ).execute()
                elif self.robot != 'Expediente':
                    return CriarCodigoUseCase(
                        page=page,
                        data_input=data_input,
                        classLogger=self.classLogger,
                        context=context,
                        robot=self.robot,
                        system_url=system_url
                    ).execute()
                else:
                    return CriarCodigoExpUseCase(
                        page=page,
                        data_input=data_input,
                        classLogger=self.classLogger,
                        context=context,
                        robot=self.robot
                    ).execute()
        except Exception as e:
            raise e

    def parse_cookie_string(self, cookie_string, domain):
        cookies = []
        cookie_pairs = cookie_string.split(';')
        for pair in cookie_pairs:
            if '=' in pair:
                name, value = pair.strip().split('=', 1)
                cookies.append({
                    'name': name,
                    'value': value,
                    'domain': domain,
                    'path': '/'
                })
        return cookies
