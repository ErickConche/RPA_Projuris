from robots.projuris.useCases.AdicionarGarantiaUseCase import AdicionarGarantiaUseCase
from playwright.sync_api import Page
from dotenv import load_dotenv
from modules.logger.Logger import Logger

load_dotenv()

class GarantiasTerceiraSituacaoUseCase:
    """
        Classe que representa o caso de uso da Terceira Situação, responsável por adicionar garantias ao processo
        no sistema Projuris.

        O caso de uso realiza as seguintes etapas:
        1. Acessa a aba de Garantias no sistema Projuris.
        2. Clica no botão "Adicionar" para iniciar o processo de inclusão de uma nova garantia.
        3. Utiliza o caso de uso AdicionarGarantiaUseCase para preencher os dados e adicionar a garantia no sistema.
    """
    
    def __init__(self, page: Page, logger: Logger, garantia_tipo: str, banco_garantia: str, agencia_garantia: str, 
                 conta_garantia: str, parcela_garantia: str, identificador_garantia: str, metodo_atualizacao_garantia: str, 
                 valor_garantia: str, depositada_pelo: str)-> None:
        """
            Inicializa os dados necessários para executar a Terceira Situação.
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
            Executa o processo de adicionar uma nova garantia ao sistema Projuris.

            Primeiro, acessa a aba de Garantias, clica no botão "Adicionar" e, em seguida, executa o caso de uso
            AdicionarGarantiaUseCase para adicionar a garantia ao processo.
        """
        # Clica em Garantias
        self.page.locator('//*[@id="projuris/ProcessoVO_3_obtem_tab__Garantiaprojuris/ProcessoVO_3_obtem"]').click()
        
        # Botão Adicionar
        self.page.locator('#label_inclui-STATIC_projuris\/GarantiaVO_3_lista > tbody > tr:nth-child(2) > td.x-btn-mc').click()
        
        # Lançamento da Garantia utilizando os dados fornecidos
        AdicionarGarantiaUseCase(
            self.page, 
            self.logger,
            self.garantia_tipo, 
            self.banco_garantia, 
            self.agencia_garantia, 
            self.conta_garantia, 
            self.parcela_garantia, 
            self.identificador_garantia, 
            self.metodo_atualizacao_garantia, 
            self.valor_garantia, 
            self.depositada_pelo
        ).execute()
