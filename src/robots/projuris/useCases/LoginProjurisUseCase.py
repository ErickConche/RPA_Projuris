import time
from playwright.sync_api import Page
from modules.logger.Logger import Logger

class LoginProjurisUseCase:
    def __init__(self, page: Page, logger: Logger, login: str, senha: str) -> None:
        """
            Classe responsável por realizar o login no sistema Projuris.
        """
        self.page = page
        self.logger = logger
        self.login = login
        self.senha = senha

    def execute(self) -> None:
        """
            Executa o processo de login no sistema Projuris.

            - Acessa a URL de login.
            - Preenche os campos de login e senha.
            - Gerencia cookies e mensagens de sessão ativa.
            - Confirma o sucesso do login.
        """
        try:
            # Navega até a página de login
            self.page.goto('https://yduqs.projuris.com.br/projuris')
            time.sleep(2)

            # Preenche o formulário de login
            self.page.fill('input[name="LOGIN"]', self.login)
            self.page.fill('input[name="SENHA"]', self.senha)
            time.sleep(1)

            # Verifica e clica na mensagem de cookies, se visível
            if self.page.locator('[aria-label="dismiss cookie message"]').is_visible():
                self.page.locator('[aria-label="dismiss cookie message"]').click()

            # Realiza o login clicando no botão de entrada
            self.page.locator('#label_ok-FORALL_projuris\/LoginVO_\*_login').click()                                                                            
            time.sleep(4)

        except Exception as e:
            self.logger.message(f"Erro ao realizar login: {e}")
            return

        # Verifica se o usuário está em uso e realiza login novamente
        if self.page.locator('#ext-gen86').is_visible():
            self.logger.message('Sessão já está ativa para este usuário. Encerrando a sessão atual e realizando um novo login.')


            # Clica em OK
            botoesOk = self.page.query_selector_all("table.x-btn.x-btn-noicon tbody.x-btn-small.x-btn-icon-small-left button.x-btn-text:has-text('OK')")

            # Verifica se foram encontrados botões com o texto "OK"
            if not botoesOk:
                raise ValueError("Nenhum botão com texto 'OK' foi encontrado!")

            # Itera sobre os botões e clica no primeiro encontrado
            primeiro_botao_ok = None

            for botao in botoesOk:
                if botao.inner_text().strip() == 'OK':  # Verifica o texto do botão
                    if primeiro_botao_ok is None:
                        primeiro_botao_ok = botao  # Define o primeiro botão encontrado
                    else:
                        # Clica no segundo botão e interrompe o loop
                        botao.click()
                        break

            # Verifica se o primeiro botão foi encontrado e clica nele
            if primeiro_botao_ok:
                primeiro_botao_ok.click()
            else:
                raise ValueError("Nenhum botão válido com texto 'OK' foi encontrado!")
        time.sleep(4)

        # Verifica a presença do seletor que confirma o login
        try:
            self.page.wait_for_selector('div[tree-node-id="PR"]', timeout=100000)
            self.logger.message("Login realizado com sucesso!")
        except Exception:
            self.logger.message("Erro ao verificar login bem-sucedido.")
