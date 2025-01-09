from robots.projuris.useCases.AdicionarLancamentoUseCase import AdicionarLancamentoUseCase
from playwright.sync_api import Page
from modules.logger.Logger import Logger

class CustasTerceiraSituacaoUseCase:
    """
        Caso de uso para a terceira situação de custas no sistema Projuris, onde a Docato capturou apenas o valor original e precisará lançar a custa.
        A RPA irá cadastrar essa movimentação.

        Esta classe é responsável por executar o fluxo de adicionar um lançamento na aba 
        de "Custas" no sistema, utilizando os dados fornecidos e chamando o caso de uso 
        de adicionar lançamento.
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
            Inicializa a classe para executar a terceira situação de custas.
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

    def execute(self) -> None:
        """
            - Clica na aba "Custas".
            - Clica no botão "Adicionar".
            - Chama o caso de uso AdicionarLancamentoUseCase para adicionar os dados do lançamento.
        """
        try:
            # Clica em Custas
            self.page.locator('//*[@id="projuris/ProcessoVO_3_obtem_tab__Lancamentoprojuris/ProcessoVO_3_obtem"]').click()
            
            # Botão Adicionar
            self.page.locator('#label_inclui-STATIC_projuris\/LancamentoVO_3_lista > tbody > tr:nth-child(2) > td.x-btn-mc').click()
            
            # Chama AdicionarLancamentoUseCase
            AdicionarLancamentoUseCase(
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

        except Exception as e:
            self.logger.message(f"Erro na execução de Custas: {e}")
