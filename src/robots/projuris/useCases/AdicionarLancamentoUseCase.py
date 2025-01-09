import time
from playwright.sync_api import Page
from modules.logger.Logger import Logger

class AdicionarLancamentoUseCase:
    """
        Caso de uso para adicionar um lançamento no sistema Projuris.

        Esta classe realiza o fluxo de preenchimento dos campos obrigatórios, seleção de opções, 
        e salva as informações utilizando a interface do Playwright.
    """

    def __init__(
            self, 
            page: Page, 
            logger: Logger, 
            processo: str,
            valor_pago: str,
            data_lancamento : str,
            valor_lancamento : str,
            metodo_atualizacao : str,
            data_pagamento : str,
            data_vencimento_lancamento : str,
            lancamento : str
            )-> None:
        """
            Inicializa a classe para o caso de uso de adicionar lançamento.
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
            - Seleciona o tipo de lançamento baseado em palavras-chave.
            - Preenche os campos obrigatórios, como data, valor e método de atualização.
            - Salva os dados no sistema.
        """
        try:
            # Listas de palavras-chave para categorização do lançamento
            palavras_1 = ["Boleto", "Apólice", "Seguro", "Garantia"]
            palavras_2 = ["Custas", "Judiciais"]
            palavras_3 = ["Honorários", "Periciais"]

            # Seleciona o tipo de lançamento
            self.page.locator('//*[@id="ID_CONTAprojuris/LancamentoVO_3_inclui"]').click()
            time.sleep(5)

            # Verifica qual categoria corresponde ao tipo de lançamento
            if isinstance(self.lancamento, str):
                if any(palavra in self.lancamento for palavra in palavras_1):
                    for _ in range(2):  # Desce 2 vezes para selecionar a opção
                        self.page.keyboard.press("ArrowDown")
                        time.sleep(2)
                elif any(palavra in self.lancamento for palavra in palavras_2):
                    for _ in range(3):  # Desce 3 vezes para selecionar a opção
                        self.page.keyboard.press("ArrowDown")
                        time.sleep(2)
                elif any(palavra in self.lancamento for palavra in palavras_3):
                    for _ in range(4):  # Desce 4 vezes para selecionar a opção
                        self.page.keyboard.press("ArrowDown")
                        time.sleep(2)
                self.page.keyboard.press("Enter")

            # Preenche a data do lançamento
            self.page.locator('//*[@id="DATAprojuris/LancamentoVO_3_inclui"]').fill(self.data_lancamento)

            # Preenche o valor do lançamento
            self.page.locator('//*[@id="VALOR_DEVIDOprojuris/LancamentoVO_3_inclui"]').fill(self.valor_lancamento)
            time.sleep(2)

            # Seleciona o método de atualização
            self.page.locator('//*[@id="ID_METODO_ATUALIZACAOprojuris/LancamentoVO_3_inclui"]').click()
            self.page.keyboard.press("ArrowDown")
            time.sleep(2)
            self.page.locator(f'//div[@id="ID_METODO_ATUALIZACAOprojuris/LancamentoVO_3_inclui_selectItem" and contains(@class, "x-combo-list-item") and text()="{self.metodo_atualizacao}"]').click()
            time.sleep(2)

            # Preenche a data de vencimento formatada
            self.page.locator('#DATA_DEVIDAprojuris\\/LancamentoVO_3_inclui').fill(self.data_vencimento_lancamento)

            # Salva o lançamento
            self.page.locator('//*[@id="label_salvar-STATIC_projuris/LancamentoVO_3_inclui"]/tbody/tr[2]/td[2]').click()
            
            self.logger.message("Lançamento adicionado com sucesso!")

        except Exception as e:
            # Loga o erro em caso de falha
            self.logger.message(f'Erro ao adicionar lançamento: {e}')
