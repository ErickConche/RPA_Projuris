import time
from playwright.sync_api import Page
from robots.projuris.useCases.ConverterParaFloatUseCase import ConverterParaFloatUseCase
from dotenv import load_dotenv
from modules.logger.Logger import Logger

load_dotenv()

class QuitacoesPrimeiraSituacaoUseCase:
    """
        Caso de uso para registrar as quitações em um processo jurídico.

        Esta classe lida com a inserção dos dados de quitação no sistema Projuris, incluindo o valor principal,
        valor devido, juros e correção, tipo de pagamento e item de quitação. A classe interage com a interface do sistema
        utilizando o Playwright para preencher os campos e realizar ações.
    """

    def __init__(self, page: Page, parcela_quitacoes: str, data_vencimento_quitacoes: str, principal_quitacoes: str, 
                 caso_acordo_condenacao: str, sentenca_condenacao: str, pago_condenacao: str, tipo_pagamento_quitacoes: str, 
                 item_quitacao: str, logger: Logger)-> None:
        """
            Inicializa o caso de uso para registrar quitações em um processo.
        """
        self.parcela_quitacoes = parcela_quitacoes
        self.data_vencimento_quitacoes = data_vencimento_quitacoes
        self.principal_quitacoes = principal_quitacoes
        self.caso_acordo_condenacao = caso_acordo_condenacao
        self.sentenca_condenacao = sentenca_condenacao
        self.pago_condenacao = pago_condenacao
        self.tipo_pagamento_quitacoes = tipo_pagamento_quitacoes
        self.item_quitacao = item_quitacao
        self.logger = logger
        self.page = page

    def execute(self)-> None:
        """
            Executa o processo de quitação, preenchendo os dados necessários e realizando as interações na página.

            Este método realiza as seguintes ações:
                1. Clica na guia de quitações.
                2. Adiciona uma nova quitação, preenchendo os campos relevantes com os dados fornecidos.
                3. Realiza os cálculos necessários (como juros e correção).
                4. Escolhe o tipo de pagamento e o item relacionado à quitação.
                5. Seleciona o cliente e salva os dados da quitação.
        """
        # Clica em Quitações
        self.page.locator('#projuris\/ProcessoVO_3_obtem_tab__Quitacaoprojuris\/ProcessoVO_3_obtem').click()
        
        # Adiciona uma nova quitação
        self.page.locator('#label_inclui-STATIC_projuris\/QuitacaoVO_3_lista > tbody').click()
        
        # Preenche os dados da parcela
        self.page.locator('#PARCELAprojuris\/QuitacaoVO_3_inclui').click()
        self.page.locator('#PARCELAprojuris\/QuitacaoVO_3_inclui').fill(self.parcela_quitacoes)
        
        # Preenche a data de vencimento
        self.page.locator('#DATA_VENCIMENTOprojuris\/QuitacaoVO_3_inclui').click()
        self.page.locator('#DATA_VENCIMENTOprojuris\/QuitacaoVO_3_inclui').fill(self.data_vencimento_quitacoes)
        
        # Verifica se é acordo ou condenação e preenche o valor principal
        if self.caso_acordo_condenacao.lower() == "acordo":
            self.page.locator('#PRINCIPAL_QUITACAOprojuris\/QuitacaoVO_3_inclui').click()
            self.page.locator('#PRINCIPAL_QUITACAOprojuris\/QuitacaoVO_3_inclui').fill(self.principal_quitacoes)
            self.devido_quitacoes = self.principal_quitacoes
        elif self.caso_acordo_condenacao.lower() in ["condenacao", "condenação", "condenaçao", "condenacão"]:
            self.page.locator('#PRINCIPAL_QUITACAOprojuris\/QuitacaoVO_3_inclui').click()
            self.page.locator('#PRINCIPAL_QUITACAOprojuris\/QuitacaoVO_3_inclui').fill(self.sentenca_condenacao)
        else:
            self.page.locator('#VALOR_DEVIDOprojuris\/QuitacaoVO_3_inclui').click()
            self.page.locator('#VALOR_DEVIDOprojuris\/QuitacaoVO_3_inclui').fill(self.pago_condenacao)
        
        # Calcula os juros e correção
        self.juros_quitacoes = ConverterParaFloatUseCase(self.principal_quitacoes).execute() - ConverterParaFloatUseCase(self.devido_quitacoes).execute()
        self.page.locator('#JUROS_CORRECAO_QUITACAOprojuris\/QuitacaoVO_3_inclui').click()
        self.juros_quitacoes = f"{self.juros_quitacoes}"
        self.page.locator('#JUROS_CORRECAO_QUITACAOprojuris\/QuitacaoVO_3_inclui').fill(self.juros_quitacoes)
        
        # Escolhe o tipo de pagamento
        self.page.locator('#ID_FORMA_PAGAMENTOprojuris\/QuitacaoVO_3_inclui').click()
        self.page.keyboard.press("ArrowDown")
        time.sleep(2)
        self.page.locator(f'//div[@id="ID_FORMA_PAGAMENTOprojuris/QuitacaoVO_3_inclui_selectItem" and contains(@class, "x-combo-list-item") and text()="{self.tipo_pagamento_quitacoes}"]').click()
        
        # Escolhe o item de quitação
        if self.item_quitacao == "Objeto":
            self.page.locator('input[type="radio"][name="ITEM_QUITACAO"][value="O"].x-form-radio.x-form-field').click()
        elif self.item_quitacao == "Honorário":
            self.page.locator('input[type="radio"][name="ITEM_QUITACAO"][value="H"].x-form-radio.x-form-field').click()
        else:
            self.logger.message("Item quitação inválido")
        
        # Escolhe o cliente
        self.page.locator('#ID_CLIENTEprojuris\/QuitacaoVO_3_inclui').click()
        self.page.keyboard.press("ArrowDown")
        time.sleep(2)
        self.page.locator('#ID_CLIENTEprojuris\/QuitacaoVO_3_inclui_selectItem').click()
        
        # Salva os dados
        self.page.locator('#label_salvar-STATIC_projuris\/QuitacaoVO_3_inclui > tbody > tr:nth-child(2) > td.x-btn-mc').click()

        self.logger.message('Quitação registrada com sucesso!')
