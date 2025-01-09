from robots.projuris.useCases.RegistrarPagamentoUseCase import RegistrarPagamentoUseCase
from modules.logger.Logger import Logger

class CustasPrimeiraSituacaoUseCase:
        """
                Caso de uso para registrar um pagamento específico no sistema Projuris.

                Esta classe executa o fluxo de selecionar o primeiro valor listado e registrar o pagamento
                utilizando o caso de uso RegistrarPagamentoUseCase.
        """
        def __init__(self, page, data_pagamento, valor_pago)-> None:
                """
                        Inicializa a classe para executar a primeira situação de custas.
                """
                self.page = page
                self.data_pagamento = data_pagamento
                self.valor_pago = valor_pago
                self.logger = Logger("log de erro")  # Inicializa o logger com um identificador específico.

        def execute(self)-> None:
                """
                        - Loga a mensagem inicial.
                        - Seleciona o primeiro valor listado.
                        - Chama o caso de uso RegistrarPagamentoUseCase para registrar o pagamento.
                """
                self.logger.message("Primeira Situação de Custas")  # Log de início

                # Clica no primeiro valor listado na coluna de custas.
                self.page.locator('div.x-grid3-cell-inner.x-grid3-col-11').nth(1).click()

                # Chama o caso de uso RegistrarPagamentoUseCase para registrar o pagamento com os dados fornecidos.
                RegistrarPagamentoUseCase(
                        self.page,
                        self.data_pagamento,
                        self.valor_pago,
                        self.logger
                ).execute()
