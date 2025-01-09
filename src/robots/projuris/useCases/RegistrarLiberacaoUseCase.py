from playwright.sync_api import Page
from dotenv import load_dotenv
from modules.logger.Logger import Logger
import time

load_dotenv()

class RegistrarLiberacao:
    """
        Classe responsável pelo processo de registro de liberação no sistema Projuris.

        A classe permite preencher os dados de uma liberação, como número do alvará, motivo da liberação,
        valor resgatado e outros, e realizar a operação no sistema por meio da interface automatizada com Playwright.
    """

    def __init__(self, page: Page, logger: Logger, data_liberacao: str, num_alvara: str, motivo_liberacao: str,
                 valor_resgatado: str, resgatado_por: str, documento_liberacao: str)-> None:
        """
            Inicializa os dados necessários para registrar a liberação.
        """
        self.page = page
        self.logger = logger
        self.data_liberacao = data_liberacao
        self.num_alvara = num_alvara
        self.motivo_liberacao = motivo_liberacao
        self.valor_resgatado = valor_resgatado
        self.resgatado_por = resgatado_por
        self.documento_liberacao = documento_liberacao

    def execute(self)-> None:
        """
            Executa o processo de registrar a liberação no sistema.

            A função preenche os campos necessários, como data da liberação, número do alvará, motivo da liberação, 
            valor resgatado, resgatado por, e documento contábil. Em seguida, realiza a operação de salvar.
        """
        # Clica em Liberações
        self.page.locator("li[id^='projuris/GarantiaVO'][id*='LiberacaoGarantiaprojuris/GarantiaVO'] span.x-tab-strip-text:has-text('Liberações')").click()
        time.sleep(2)

        # Clica em Adicionar
        self.page.locator("table[id^='label_inclui-STATIC_projuris/LiberacaoGarantiaVO'] button.x-btn-text:has-text('Adicionar')").click()
        time.sleep(2)

        # Preenche a data da liberação
        self.page.locator("input[id^='DATA_LIBERACAOprojuris/LiberacaoGarantiaVO_'][name='DATA_LIBERACAO']").click()
        self.page.locator("input[id^='DATA_LIBERACAOprojuris/LiberacaoGarantiaVO_'][name='DATA_LIBERACAO']").fill(self.data_liberacao)

        # Preenche o número do Alvará
        self.page.locator("input[id^='NUMERO_ALVARAprojuris/LiberacaoGarantiaVO']").click()
        self.page.locator("input[id^='NUMERO_ALVARAprojuris/LiberacaoGarantiaVO']").fill(self.num_alvara)

        # Seleciona o motivo da liberação
        self.page.locator("img[src='/scripts/ext/resources/images/default/s.gif'][class='x-form-trigger x-form-arrow-trigger']").nth(0).click()
        time.sleep(3)
        if self.motivo_liberacao == "Levantamento" or "levantamento":
            self.page.locator('div.x-combo-list-item:has-text("Baixa da Garantia por Despesa")').click()
        elif self.motivo_liberacao == "Resgate" or "resgate":
            self.page.locator('div.x-combo-list-item:has-text("Recuperação da Garantia")').click()
        else:
            self.logger.message(f"Motivo da Liberação inválido")

        # Preenche o valor resgatado
        self.page.locator("input[id^='VALOR_RESGATADOprojuris/LiberacaoGarantiaVO']").click()
        self.page.locator("input[id^='VALOR_RESGATADOprojuris/LiberacaoGarantiaVO']").fill(self.valor_resgatado)

        # Seleciona quem resgatou
        if self.resgatado_por == "Cliente" or "cliente":
            self.page.locator('input[type="radio"][name="RESGATADOR"][value="C"].x-form-radio.x-form-field').click()
        else:
            self.page.locator('input[type="radio"][name="RESGATADOR"][value="A"].x-form-radio.x-form-field').click()

        # Preenche o documento contábil da liberação
        self.page.locator("input[id^='DOC_CONTABIL_CUSTOMprojuris/LiberacaoGarantiaVO']").click()
        self.page.locator("input[id^='DOC_CONTABIL_CUSTOMprojuris/LiberacaoGarantiaVO']").fill(self.documento_liberacao)

        # Clica em Salvar
        self.page.locator("table[id^='label_salvar-STATIC_projuris/LiberacaoGarantiaVO'][id$='_inclui']").click()
