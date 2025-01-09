from robots.projuris.useCases.AdicionarGarantiaUseCase import AdicionarGarantiaUseCase
from playwright.sync_api import Page
from dotenv import load_dotenv
from modules.logger.Logger import Logger
import time
from robots.projuris.useCases.RegistrarLiberacaoUseCase import RegistrarLiberacao

load_dotenv()

class GarantiasSegundaSituacaoUseCase:
    """
        Classe que representa o caso de uso da Segunda Situação, que inclui o processo de adicionar garantia 
        e registrar a liberação no sistema Projuris.

        Este caso de uso realiza duas etapas principais:
        1. Adicionar uma nova garantia no sistema.
        2. Registrar a liberação, preenchendo os campos necessários com as informações fornecidas.
    """

    def __init__(self, page: Page, logger: Logger, data_liberacao: str, num_alvara: str, motivo_liberacao: str,
                 valor_resgatado: str, resgatado_por: str, documento_liberacao: str, garantia_tipo: str, 
                 banco_garantia: str, agencia_garantia: str, conta_garantia: str, parcela_garantia: str, 
                 identificador_garantia: str, metodo_atualizacao_garantia: str, valor_garantia: str, 
                 depositada_pelo: str)-> None:
        """
            Inicializa os dados necessários para executar a Segunda Situação.
        """
        self.page = page
        self.logger = logger
        self.data_liberacao = data_liberacao
        self.num_alvara = num_alvara
        self.motivo_liberacao = motivo_liberacao
        self.valor_resgatado = valor_resgatado
        self.resgatado_por = resgatado_por
        self.documento_liberacao = documento_liberacao
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
            Executa o processo de adicionar uma nova garantia e registrar a liberação no sistema.

            Primeiro, a função realiza a ação de adicionar uma nova garantia no sistema, utilizando as informações
            fornecidas na inicialização. Em seguida, registra a liberação, preenchendo os campos necessários e realizando
            a operação de salvar.
        """
        # Clica em Adicionar Garantia
        self.page.locator('#label_inclui-STATIC_projuris\/GarantiaVO_3_lista > tbody > tr:nth-child(2) > td.x-btn-mc').click()   
        
        # Executa o caso de uso para adicionar garantia
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
        
        # Executa o caso de uso para registrar liberação
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
