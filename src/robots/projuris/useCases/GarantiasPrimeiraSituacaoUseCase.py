import time
from playwright.sync_api import Page
from dotenv import load_dotenv
from modules.logger.Logger import Logger
from robots.projuris.useCases.RegistrarLiberacaoUseCase import RegistrarLiberacao

load_dotenv()

class GarantiasPrimeiraSituacaoUseCase:
    """
        Caso de uso para processar a primeira situação de liberação de valores.

        Esta classe lida com a liberação de valores em uma situação específica, clicando no elemento correspondente
        na página e registrando a liberação através do caso de uso `RegistrarLiberacao`.
    """

    def __init__(self, page: Page, logger: Logger, data_liberacao: str, num_alvara: str, motivo_liberacao: str,
                 valor_resgatado: str, resgatado_por: str, documento_liberacao: str)-> None:
        """
            Inicializa o caso de uso da Primeira Situação de liberação de valores.
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
            Executa a ação de registrar a liberação de valores.

            Este método realiza a interação com a página da aplicação, clicando no valor desejado, e então
            chama o caso de uso `RegistrarLiberacao` para registrar os detalhes da liberação.

            O processo inclui:
                1. Clicar no segundo valor na página.
                2. Chamar o caso de uso `RegistrarLiberacao` com os dados fornecidos para realizar o registro.

            Chama o método `execute` da classe `RegistrarLiberacao` para concluir o processo de liberação.
        """
        # Clica no segundo valor
        self.page.locator('div.x-grid3-row.grid1.x-grid3-row-last > table > tbody > tr > td.x-grid3-cell-last.x-grid3-td-8 > div > div').click()
        
        # Registra a liberação
        RegistrarLiberacao(
            self.page,
            self.logger,
            self.data_liberacao,
            self.num_alvara,
            self.motivo_liberacao,
            self.valor_resgatado,
            self.resgatado_por,
            self.documento_liberacao
        ).execute()
