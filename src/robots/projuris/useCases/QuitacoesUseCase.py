from playwright.sync_api import Page
from modules.logger.Logger import Logger

from robots.projuris.useCases.QuitacoesPrimeiraSituacaoUseCase import QuitacoesPrimeiraSituacaoUseCase
from robots.projuris.useCases.QuitacoesSegundaSituacaoUseCase import QuitacoesSegundaSituacaoUseCase

class QuitacoesUseCase:
    """
        Classe responsável pelo processo de quitações no sistema Projuris.

        A classe gerencia as duas situações possíveis para quitações: 
        - Novo pagamento
        - Pagamento já realizado
    """

    def __init__(self, page: Page, parcela_quitacoes: str, data_vencimento_quitacoes: str, 
                 principal_quitacoes: str, caso_acordo_condenacao: str, sentenca_condenacao: str, 
                 pago_condenacao: str, tipo_pagamento_quitacoes: str, item_quitacao: str, 
                 situacao_quitacoes: str, devido_quitacoes:str, data_pagamento_quitacoes:str, valor_pago_quitacoes:str, logger: Logger)-> None:
        """
            Inicializa os dados necessários para o processamento das quitações.
        """
        self.page = page
        self.parcela_quitacoes = parcela_quitacoes
        self.data_vencimento_quitacoes = data_vencimento_quitacoes
        self.principal_quitacoes = principal_quitacoes
        self.caso_acordo_condenacao = caso_acordo_condenacao
        self.sentenca_condenacao = sentenca_condenacao
        self.pago_condenacao = pago_condenacao
        self.tipo_pagamento_quitacoes = tipo_pagamento_quitacoes
        self.item_quitacao = item_quitacao
        self.situacao_quitacoes = situacao_quitacoes
        self.devido_quitacoes = devido_quitacoes
        self.data_pagamento_quitacoes = data_pagamento_quitacoes
        self.valor_pago_quitacoes = valor_pago_quitacoes
        self.logger = logger

    def execute(self)-> None:
        """
            Executa o processo de quitação baseado na situação informada.

            Dependendo da situação da quitação, o processo será direcionado para a primeira ou segunda situação.
            A primeira situação envolve um novo pagamento, enquanto a segunda situação trata de uma quitação já realizada.
        """
        try:
            # Primeira Situação
            if self.situacao_quitacoes == "Novo Pagamento":
                QuitacoesPrimeiraSituacaoUseCase(
                    self.page,
                    self.parcela_quitacoes,
                    self.data_vencimento_quitacoes,
                    self.principal_quitacoes,
                    self.caso_acordo_condenacao,
                    self.sentenca_condenacao,
                    self.pago_condenacao,
                    self.tipo_pagamento_quitacoes,
                    self.item_quitacao,
                    self.logger
                ).execute()
                
                self.logger.message("Primeira Situação-Quitações finalizada.")
                return

            # Segunda Situação
            else:
                QuitacoesSegundaSituacaoUseCase(
                    self.page,
                    self.devido_quitacoes,
                    self.data_pagamento_quitacoes,
                    self.valor_pago_quitacoes,
                    self.logger
                ).execute()

                self.logger.message("Segunda Situação-Quitações finalizada.")
                return

        except Exception as e:
            self.logger.message(f"Erro ao processar quitação: {e}")
