import time
from robots.projuris.useCases.CustasPrimeiraSituacaoUseCase import CustasPrimeiraSituacaoUseCase
from robots.projuris.useCases.CustasSegundaSituacaoUseCase import CustasSegundaSituacaoUseCase
from robots.projuris.useCases.CustasTerceiraSituacaoUseCase import CustasTerceiraSituacaoUseCase
from playwright.sync_api import Page
from modules.logger.Logger import Logger

class CustasUseCase:
    """
        Caso de uso para processar diferentes situações relacionadas às custas de um processo.

        Essa classe verifica as condições específicas de valores e executa os casos de uso apropriados 
        para cada situação, incluindo a Primeira, Segunda ou Terceira Situação.
    """

    def __init__(
            self, 
            page : Page, 
            logger:Logger, 
            processo:str, 
            valor_pago:str, 
            data_lancamento:str, 
            valor_lancamento:str, 
            metodo_atualizacao:str, 
            data_pagamento:str,
            data_vencimento_lancamento:str, 
            lancamento:str
            )-> None:
        
        """
            Inicializa o objeto CustasUseCase com os parâmetros necessários.
        """
        self.page = page
        self.logger = logger
        self.processo = processo
        self.valor_pago = valor_pago
        self.data_lancamento = data_lancamento
        self.valor_lancamento = valor_lancamento
        self.metodo_atualizacao = metodo_atualizacao
        self.data_pagamento = data_pagamento
        self.data_vencimento_lancamento = data_vencimento_lancamento
        self.lancamento = lancamento

    def execute(self)-> None:
        """
            Executa o processamento das custas de acordo com a situação identificada.

            Situações:
                1. Primeira Situação: Quando o primeiro e o segundo valores de custas são iguais.
                2. Segunda Situação: Quando o segundo valor está vazio ou é igual ao primeiro.
                3. Terceira Situação: Qualquer outra condição.
        """
        try:
            # Acessa a página de custas
            self.page.locator('#projuris\/ProcessoVO_3_obtem_tab__Lancamentoprojuris\/ProcessoVO_3_obtem').click()
            time.sleep(5)

            # Obtém os valores das custas
            primeiro_valor_custas = self.page.locator('div.x-grid3-cell-inner.x-grid3-col-11').nth(1).inner_text().strip()
            segundo_valor_custas = self.page.locator('div.x-grid3-cell-inner.x-grid3-col-11').nth(2).inner_text().strip()
            terceiro_valor_custas = self.page.locator('div.x-grid3-cell-inner.x-grid3-col-11').nth(3).inner_text().strip()

            self.logger.message(f"Primeiro valor: {primeiro_valor_custas}")
            self.logger.message(f"Segundo valor: {segundo_valor_custas}")
            self.logger.message(f"Terceiro valor: {terceiro_valor_custas}")

            # Primeira Situação
            if primeiro_valor_custas == segundo_valor_custas: 
                CustasPrimeiraSituacaoUseCase(
                    self.page,
                    self.data_pagamento,
                    self.valor_pago
                ).execute()
                self.logger.message("Primeira Situação-Custas finalizada.")
                return

            # Segunda Situação
            elif primeiro_valor_custas == segundo_valor_custas or not segundo_valor_custas: #
                CustasSegundaSituacaoUseCase(
                    self.page,
                    self.logger,
                    self.processo,
                    self.valor_lancamento,
                    self.data_lancamento,
                    self.metodo_atualizacao,
                    self.valor_pago,
                    self.data_pagamento,
                    self.data_vencimento_lancamento,
                    self.lancamento,
                    primeiro_valor_custas=primeiro_valor_custas,
                    segundo_valor_custas=segundo_valor_custas
                ).execute()
                self.logger.message("Segunda Situação-Custas finalizada.")
                return

            # Terceira Situação
            else:
                CustasTerceiraSituacaoUseCase(
                    self.page,
                    self.logger,
                    self.processo,
                    self.valor_pago,
                    self.data_lancamento,
                    self.valor_lancamento,
                    self.metodo_atualizacao,
                    self.data_pagamento,
                    self.data_vencimento_lancamento,
                    self.lancamento
                ).execute()
                self.logger.message("Terceira Situação-Custas finalizada.")
                return

        except Exception as e:
            self.logger.message(f"Erro ao processar custas: {e}")
