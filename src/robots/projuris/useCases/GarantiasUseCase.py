import time
from robots.projuris.useCases.GarantiasPrimeiraSituacaoUseCase import GarantiasPrimeiraSituacaoUseCase
from robots.projuris.useCases.GarantiasSegundaSituacaoUseCase import GarantiasSegundaSituacaoUseCase
from robots.projuris.useCases.GarantiasTerceiraSituacaoUseCase import GarantiasTerceiraSituacaoUseCase
from playwright.sync_api import Page
from modules.logger.Logger import Logger

class GarantiasUseCase:
    """
        Caso de uso para processar diferentes situações relacionadas às garantias de um processo.

        Essa classe verifica as condições específicas de valores de garantia e executa os casos de uso apropriados
        para cada situação, incluindo a Primeira, Segunda ou Terceira Situação.
    """

    def __init__(self, page:Page, data_liberacao:str, num_alvara:str, motivo_liberacao:str, valor_resgatado:str, resgatado_por:str,
                 documento_liberacao:str, garantia_tipo:str, banco_garantia:str, agencia_garantia:str, conta_garantia:str, parcela_garantia:str,
                 identificador_garantia:str, metodo_atualizacao_garantia:str, valor_garantia:str, depositada_pelo:str, logger:Logger)-> None:
        """
        Inicializa o objeto GarantiasUseCase com os parâmetros necessários.
        """
        self.page = page
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
        self.logger = logger

    def execute(self) -> None:
        """
            Executa o processamento das garantias de acordo com a situação identificada.

            Situações:
                1. Primeira Situação: Quando o primeiro e o segundo valores de garantia são válidos e diferentes.
                2. Segunda Situação: Quando o primeiro valor de garantia é válido e o segundo é vazio ou igual ao primeiro.
                3. Terceira Situação: Qualquer outra condição.
        """
        try:
            # Acessa a página de garantias
            self.page.locator('#projuris\/ProcessoVO_3_obtem_tab__Garantiaprojuris\/ProcessoVO_3_obtem').click()
            time.sleep(3)

            # Obtém os valores das garantias
            primeiro_valor_garantia = self.page.locator('div.x-grid3-row.x-grid3-row-first > table > tbody > tr > td.x-grid3-cell-last.x-grid3-td-8 > div > div').first.inner_text().strip()
            segundo_valor_garantia = None
            terceiro_valor_garantia = None
            quarto_valor_garantia = None

            # Verifica se há 3 ou mais valores de garantia
            if self.page.locator("td.x-grid3-col.x-grid3-cell.x-grid3-td-8.x-grid3-cell-last[style='width: 144px;text-align: right;']").count() >= 3:
                segundo_valor_garantia = self.page.locator("td.x-grid3-col.x-grid3-cell.x-grid3-td-8.x-grid3-cell-last[style='width: 144px;text-align: right;']").nth(1).inner_text().strip()
                if self.page.locator("td.x-grid3-col.x-grid3-cell.x-grid3-td-8.x-grid3-cell-last[style='width: 144px;text-align: right;']").count() >= 4:
                    terceiro_valor_garantia = self.page.locator("td.x-grid3-col.x-grid3-cell.x-grid3-td-8.x-grid3-cell-last[style='width: 144px;text-align: right;']").nth(2).inner_text().strip()
                    if self.page.locator("td.x-grid3-col.x-grid3-cell.x-grid3-td-8.x-grid3-cell-last[style='width: 144px;text-align: right;']").count() >= 5:
                        quarto_valor_garantia = self.page.locator("td.x-grid3-col.x-grid3-cell.x-grid3-td-8.x-grid3-cell-last[style='width: 144px;text-align: right;']").nth(3).inner_text().strip()
                    else:
                        quarto_valor_garantia = False
                else:
                    terceiro_valor_garantia = False
            elif self.page.locator("td.x-grid3-col.x-grid3-cell.x-grid3-td-8.x-grid3-cell-last[style='width: 144px;text-align: right;']").count() <= 2:
                segundo_valor_garantia = False

            self.logger.message(f"Primeiro valor: {primeiro_valor_garantia}")
            self.logger.message(f"Segundo valor: {segundo_valor_garantia}")
            self.logger.message(f"Terceiro valor: {terceiro_valor_garantia}")
            self.logger.message(f"Quarto valor: {quarto_valor_garantia}")

            # Primeira Situação
            if primeiro_valor_garantia and segundo_valor_garantia:
                GarantiasPrimeiraSituacaoUseCase(
                    self.page,
                    self.logger,
                    self.data_liberacao,
                    self.num_alvara,
                    self.motivo_liberacao,
                    self.valor_resgatado,
                    self.resgatado_por,
                    self.documento_liberacao
                ).execute()
                self.logger.message("Primeira Situação-Garantias finalizada.")
                return

            # Segunda Situação
            elif not primeiro_valor_garantia or not segundo_valor_garantia:
                GarantiasSegundaSituacaoUseCase(
                    self.page,
                    self.logger,
                    self.data_liberacao,
                    self.num_alvara,
                    self.motivo_liberacao,
                    self.valor_resgatado,
                    self.resgatado_por,
                    self.documento_liberacao,
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
                self.logger.message("Segunda Situação-Garantias finalizada.")
                return

            # Terceira Situação
            else:
                GarantiasTerceiraSituacaoUseCase(
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
                self.logger.message("Terceira Situação-Garantias finalizada.")
                return

        except Exception as e:
            self.logger.message(f"Erro ao processar garantia: {e}")
