from playwright.sync_api import Page
from dotenv import load_dotenv
from modules.logger.Logger import Logger
import time

load_dotenv()

class QuitacoesSegundaSituacaoUseCase:
    def __init__(self, page: Page, devido_quitacoes: str, data_pagamento_quitacoes: str, 
                valor_pago_quitacoes: str, logger: Logger)-> None:  
        """
            Inicializa a classe com os parâmetros.
        """
        self.page: Page = page
        self.devido_quitacoes: str = devido_quitacoes
        self.data_pagamento_quitacoes: str = data_pagamento_quitacoes
        self.valor_pago_quitacoes: str = valor_pago_quitacoes
        self.logger: Logger = logger 

    def execute(self) -> None:
        """
            Executa a lógica para registrar o pagamento de quitação.

            Realiza as seguintes ações na interface:
            - Clica na aba "Quitações".
            - Localiza e seleciona a quitação pelo valor devido.
            - Insere a data de pagamento.
            - Insere o valor pago.
            - Salva a operação.
        """
        # Clica em Quitações
        self.page.locator('#projuris\/ProcessoVO_3_obtem_tab__Quitacaoprojuris\/ProcessoVO_3_obtem').click()

        # Clica na quitação
        self.page.locator(f"text='{self.devido_quitacoes}'").nth(1).click()
        time.sleep(2)

        # Clica em Efetuar Baixa
        botoes = self.page.query_selector_all("table[id^='label_efetuarBaixa-FORONE_projuris/QuitacaoVO_'] button.x-btn-text:has-text('Efetuar Baixa')")

        # Verifica se foram encontrados botões com o texto "Efetuar Baixa"
        if not botoes:
            raise ValueError("Nenhum botão com texto 'Efetuar Baixa' foi encontrado!")

        # Variável para armazenar o último ID válido
        ultimo_id_botao_efetuar_baixa = None

        # Itera sobre todos os botões encontrados
        for botao in botoes:
            if botao.inner_text().strip() == 'Efetuar Baixa':  # Verifica o texto do botão
                ultimo_id_botao_efetuar_baixa = botao.get_attribute('id').strip()  # Atualiza com o último ID encontrado

        # Realiza o clique no último botão encontrado
        if ultimo_id_botao_efetuar_baixa:
            # Realiza o clique no último botão com o ID armazenado
            self.page.locator(f'#{ultimo_id_botao_efetuar_baixa}').click()
        else:
            raise ValueError("Nenhum botão válido com texto 'Efetuar Baixa' foi encontrado!")

        # Opção com nth(). caso o código acima não esteja funcionando
        #self.page.locator("table[id^='label_efetuarBaixa-FORONE_projuris/QuitacaoVO_'] button.x-btn-text:has-text('Efetuar Baixa')").last.click()

        # Preenche a data do pagamento
        self.page.locator("input[id^='DATA_PAGAMENTOprojuris/QuitacaoVO_'][name='DATA_PAGAMENTO']").click()
        self.page.locator("input[id^='DATA_PAGAMENTOprojuris/QuitacaoVO_'][name='DATA_PAGAMENTO']").fill(self.data_pagamento_quitacoes)

        # Preenche o valor pago
        self.page.locator("input[id^='VALOR_PAGOprojuris/QuitacaoVO_'][name='VALOR_PAGO']").click()
        self.page.locator("input[id^='VALOR_PAGOprojuris/QuitacaoVO_'][name='VALOR_PAGO']").fill(self.valor_pago_quitacoes)

        # Salva a operação
        self.page.locator("table[id^='label_salvar-STATIC_projuris/QuitacaoVO_']").click()

        # Log da mensagem de sucesso
        self.logger.message('Baixa da quitação registrada com sucesso!')
