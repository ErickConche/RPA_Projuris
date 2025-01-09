from playwright.sync_api import Page
from dotenv import load_dotenv
from modules.logger.Logger import Logger
import time

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class AdicionarGarantiaUseCase:
    """
        Caso de uso para adicionar uma garantia no sistema Projuris.

        Esta classe realiza o fluxo de preenchimento dos campos obrigatórios, seleção de opções, 
        e salva as informações utilizando a interface do Playwright.
    """

    def __init__(self, page: Page, logger: Logger, garantia_tipo: str, banco_garantia: str, 
                 agencia_garantia: str, conta_garantia: str, parcela_garantia: str, 
                 identificador_garantia: str, metodo_atualizacao_garantia: str, 
                 valor_garantia: str, depositada_pelo: str)-> None:
        """
            Inicializa a classe para o caso de uso de adicionar garantia.
        """
        self.page = page
        self.logger = logger
        self.garantia_tipo = garantia_tipo
        self.banco_garantia = banco_garantia
        self.agencia_garantia = agencia_garantia
        self.conta_garantia = conta_garantia
        self.parcela_garantia = parcela_garantia
        self.identificador_garantia = identificador_garantia
        self.metodo_atualizacao_garantia = metodo_atualizacao_garantia
        self.valor_garantia = valor_garantia
        self.depositada_pelo = depositada_pelo

    def execute(self)-> None:
        """
            - Preenche os campos obrigatórios como tipo de garantia, banco, conta, etc.
            - Seleciona opções específicas no formulário.
            - Salva os dados no sistema.
        """
        try:
            # Seleciona o tipo de garantia
            self.page.locator('#ID_GARANTIAprojuris\\/GarantiaVO_3_inclui').click()
            self.page.keyboard.press("ArrowDown")
            time.sleep(2)
            self.page.locator(f'//div[@id="ID_GARANTIAprojuris/GarantiaVO_3_inclui_selectItem" and contains(@class, "x-combo-list-item") and text()="{self.garantia_tipo}"]').click()
            time.sleep(2)

            # Preenche os campos obrigatórios
            self.page.locator('#ID_BANCOprojuris\\/GarantiaVO_3_inclui').fill(self.banco_garantia)
            self.page.locator('#AGENCIAprojuris\\/GarantiaVO_3_inclui').fill(self.agencia_garantia)
            self.page.locator('#CONTA_JUDICIALprojuris\\/GarantiaVO_3_inclui').fill(self.conta_garantia)
            self.page.locator('#PARCELAprojuris\\/GarantiaVO_3_inclui').fill(self.parcela_garantia)
            self.page.locator('#IDENTIFICADORprojuris\\/GarantiaVO_3_inclui').fill(self.identificador_garantia)

            # Seleciona o método de atualização
            self.page.locator('#ID_METODO_ATUALIZACAOprojuris\\/GarantiaVO_3_inclui').click()
            self.page.keyboard.press("ArrowDown")
            time.sleep(2)
            self.page.locator(f'//div[@id="ID_METODO_ATUALIZACAOprojuris/GarantiaVO_3_inclui_selectItem" and contains(@class, "x-combo-list-item") and text()="{self.metodo_atualizacao_garantia}"]').click()
            time.sleep(1)

            # Preenche o valor da garantia
            self.page.locator('#PRINCIPAL_GARANTIAprojuris\\/GarantiaVO_3_inclui').fill(self.valor_garantia)

            # Seleciona o responsável pelo depósito
            if self.depositada_pelo.lower() in ["depósito", "deposito"]:
                self.page.locator("//input[@type='radio' and @name='AUTOR_GARANTIA' and @value='C']").click()
            else:
                self.page.locator("//input[@type='radio' and @name='AUTOR_GARANTIA' and @value='A']").click()

            # Salva a garantia
            time.sleep(1)
            self.page.locator('#label_salvar-STATIC_projuris\\/GarantiaVO_3_inclui > tbody').click()
            self.logger.message("Garantia adicionada com sucesso!")

        except Exception as e:
            # Log de erro em caso de falha
            self.logger.message(f'Erro ao adicionar garantia: {e}')
