import time
from playwright.sync_api import Page
from robots.projuris.useCases.AdicionarLancamentoUseCase import AdicionarLancamentoUseCase
from robots.projuris.useCases.NormalizeValorUseCase import NormalizeValorUseCase
from modules.logger.Logger import Logger

class CustasSegundaSituacaoUseCase:
    """
        Caso de uso para a segunda situação de custas no sistema Projuris, onde a Docato captura uma movimentação de liberação, 
        porém o valor original ainda não está cadastrado no Projuris.
        Nesse caso, a RPA irá primeiramente cadastrar a movimentação e posteriormente a liberação.


        Esta classe é responsável por executar o fluxo completo para registrar o pagamento de um lançamento na aba 
        "Custas", utilizando os dados fornecidos e interagindo com a interface do sistema.
    """

    def __init__(
            self, 
            page: Page, 
            logger: Logger, 
            processo:str, 
            valor_lancamento: str, 
            data_lancamento: str, 
            metodo_atualizacao: str, 
            valor_pago: str,
            data_pagamento: str, 
            data_vencimento_lancamento: str, 
            lancamento: str, 
            primeiro_valor_custas: str, 
            segundo_valor_custas: str
            )-> None:
        """
        Inicializa a classe para executar a segunda situação de custas.
        """
        self.page: Page = page
        self.logger = logger
        self.processo = processo
        self.lancamento = lancamento
        self.data_lancamento = data_lancamento
        self.valor_lancamento = valor_lancamento
        self.data_pagamento = data_pagamento
        self.metodo_atualizacao = metodo_atualizacao
        self.valor_pago = valor_pago
        self.data_vencimento_lancamento = data_vencimento_lancamento
        self.primeiro_valor_custas = primeiro_valor_custas
        self.segundo_valor_custas = segundo_valor_custas

    def execute(self) -> None:
        """
            - Registra uma mensagem de logger com os valores de custas.
            - Adiciona um lançamento.
            - Registra o pagamento do lançamento, preenchendo os campos necessários com os dados capturados.
            - Salva o registro do pagamento.
        """
        # Log dos valores de custas
        self.logger.message(f"Os valores são diferentes: {self.primeiro_valor_custas} e {self.segundo_valor_custas}")

        # Botão Adicionar
        self.page.locator('//*[@id="label_inclui-STATIC_projuris/LancamentoVO_3_lista"]/tbody/tr[2]/td[2]/em').click()
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

        time.sleep(7)

        # Clica em Custas
        self.page.locator('//*[@id="projuris/ProcessoVO_3_obtem_tab__Lancamentoprojuris/ProcessoVO_3_obtem"]').click(position={"x": 0.5, "y": 0.5})
        valor_lancamento_formatado = NormalizeValorUseCase(self.valor_lancamento).execute()

        # Clica no novo elemento criado
        self.page.locator(f'//div[contains(@class, "link-comum") and contains(@class, "x-tabs-text") and text()="{valor_lancamento_formatado}"]').last.click()
        time.sleep(6)

        # Acessa "Registrar Pagamento"
        self.page.locator('//table[contains(@id, "label_efetuaBaixaLanc-FORONE_projuris/LancamentoVO")]', has_text="Registrar Pagamento").last.click()
        time.sleep(4)

        # Preenche "Data de Pagamento"
        self.page.locator('//input[contains(@class, "x-form-text x-form-field x-required") and starts-with(@id, "DATA_REALIZACAOprojuris/LancamentoVO")]').click()
        self.page.locator('//input[contains(@class, "x-form-text x-form-field x-required") and starts-with(@id, "DATA_REALIZACAOprojuris/LancamentoVO")]').fill(self.data_pagamento)

        # Preenche "Valor Pago"
        self.page.locator('//input[contains(@class, "x-form-text x-form-field x-required") and starts-with(@id, "VALOR_REALIZADOprojuris/LancamentoVO") and @name="VALOR_REALIZADO"]').click()
        self.page.locator('//input[contains(@class, "x-form-text x-form-field x-required") and starts-with(@id, "VALOR_REALIZADOprojuris/LancamentoVO") and @name="VALOR_REALIZADO"]').fill(self.valor_pago)

        # Salva o pagamento
        self.page.locator('//table[contains(@id, "label_salvar-STATIC_projuris/LancamentoVO")]', has_text="Salvar").click()
        time.sleep(2)
        self.logger.message('Pagamento registrado com sucesso!')
