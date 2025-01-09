from playwright.sync_api import Page
from dotenv import load_dotenv
import time
from modules.logger.Logger import Logger

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class RegistrarPagamentoUseCase:
    """
        Caso de uso para registrar um pagamento no sistema Projuris.

        Esta classe executa o fluxo de preencher os campos obrigatórios de data e valor do pagamento, 
        e salva os dados no sistema utilizando a interface do Playwright.
    """

    def __init__(self, page: Page, data_pagamento: str, valor_pago: str, logger: Logger)-> None:
        """
            Inicializa a classe para o caso de uso de registrar pagamento.
        """
        self.page = page
        self.data_pagamento = data_pagamento
        self.valor_pago = valor_pago
        self.logger = logger

    def execute(self)-> None:
        """
            - Clica no botão "Registrar Pagamento".
            - Preenche os campos "Data de Pagamento" e "Valor Pago".
            - Salva o registro.
        """
        try:
            # Clica no botão "Registrar Pagamento"
            self.page.locator("(//button[contains(@class, 'x-btn-text') and normalize-space(text())='Registrar Pagamento'])[2]").click()
            time.sleep(2)

            # Preenche o campo "Data de Pagamento"
            if self.page.locator("input[id^='DATA_REALIZACAOprojuris/LancamentoVO_'][name='DATA_REALIZACAO']").is_visible():
                self.page.locator("input[id^='DATA_REALIZACAOprojuris/LancamentoVO_'][name='DATA_REALIZACAO']").click()
                self.page.locator("input[id^='DATA_REALIZACAOprojuris/LancamentoVO_'][name='DATA_REALIZACAO']").fill(self.data_pagamento)

            # Preenche o campo "Valor Pago"
            if self.page.locator("input[id^='VALOR_REALIZADOprojuris\\/LancamentoVO_'][name='VALOR_REALIZADO']").is_visible():
                self.page.locator("input[id^='VALOR_REALIZADOprojuris\\/LancamentoVO_'][name='VALOR_REALIZADO']").click()
                self.page.locator("input[id^='VALOR_REALIZADOprojuris\\/LancamentoVO_'][name='VALOR_REALIZADO']").fill(self.valor_pago)

            # Clica no botão de salvar
            self.page.locator("//table[contains(@id, 'label_salvar-STATIC_projuris/LancamentoVO_')]").click()
            self.logger.message('Pagamento registrado com sucesso!')

        except Exception as e:
            # Log de erro caso o registro falhe
            self.logger.message(f'Erro ao registrar pagamento: {e}')
