import time
from modules.logger.Logger import Logger
from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)


class FormularioGeralUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderModel,
        classLogger: Logger,
        robot: str,
        iframe: Frame
    ):
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.robot = robot
        self.iframe = iframe

    def execute(self):
        try:
            '''
            *** Informações Tópico Geral ***
            '''
            self.classLogger.message('Iniciando cadastro das informações da aba Geral')
            time.sleep(5)
            if self.page.query_selector('tour-popup') and self.page.query_selector('tour-popup').is_visible():
                self.page.query_selector('tour-popup > tour-popup-actions > button').click()
                time.sleep(3)
            if self.page.query_selector('tour-popup'):
                self.page.query_selector('tour-popup > tour-popup-actions > button').click()
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos gerais iniciado")
            time.sleep(5)
            self.iframe.query_selector('[name="CLI_AcaoEspecial"]').click()
            self.page.query_selector(f'[title="{self.data_input.acao_especial}"]').click()
            self.iframe.query_selector('[name="Cliente"]').type(self.data_input.documento_cliente_principal)
            time.sleep(20)
            if not self.page.query_selector(f'[title="{self.data_input.cliente_principal}"]'):
                # TO DO: CADASTRAR CLIENTE PRINCIPAL
                pass
            self.page.query_selector(f'[title="{self.data_input.cliente_principal}"]').dblclick()
            self.iframe.wait_for_selector('[name="CondicaoCliente"]')
            self.iframe.query_selector('[name="CondicaoCliente"]').type(self.data_input.condicao_cliente)
            time.sleep(5)
            self.page.query_selector(f'[title="{self.data_input.condicao_cliente.upper()}"]').dblclick()
            self.iframe.query_selector('[name="CLI_NumeroProcesso"]').type(num_pre_cadastro)
            self.iframe.query_selector('[name="Adverso"]').type(self.data_input.adverso_principal)
            time.sleep(20)
            self.page.query_selector(f'[title="{self.data_input.adverso_principal.upper()}"]').dblclick()
            time.sleep(2)
            self.iframe.query_selector('[name="CondicaoAdverso"]').type(self.data_input.condição_adverso)
            time.sleep(2)
            self.iframe.query_selector('[name="Advogado"]').type(self.data_input.advogado_interno_vale)
            time.sleep(5)
            list_selectors = self.page.query_selector_all(f'[title="{self.data_input.advogado_interno_vale}"]')
            list_selectors[len(list_selectors)-1].dblclick()
            time.sleep(5)
            self.iframe.query_selector('[id="RegistroNivel1Edt"]').type(self.data_input.unidade_controle)
            time.sleep(5)
            list_selectors = self.page.query_selector_all(f'[title="{self.data_input.unidade_controle.title()}"]')
            list_selectors[len(list_selectors)-1].dblclick()
            time.sleep(1)
            self.iframe.query_selector('[name="Categoria"]').type(self.data_input.natureza)
            time.sleep(5)
            self.page.query_selector(f'[title="{self.data_input.natureza.title()}"]').dblclick()
            time.sleep(5)
            if 'trabalhista' in self.data_input.natureza.lower():
                self.iframe.query_selector('[name="CLI_TipoNatureza"]').type(self.data_input.tipo)
                time.sleep(4)
                self.page.query_selector(f'[title="{self.data_input.tipo.title()}"]').dblclick()
            time.sleep(5)
            self.iframe.query_selector('[name="Tipo"]').type(self.data_input.tipo_acao.split('  ')[0])
            time.sleep(2)
            self.page.query_selector(f'[title="{self.data_input.tipo_acao.split("  ")[0].upper()}"]').dblclick()
            time.sleep(2)
            self.iframe.query_selector('[name="Unidade"]').type(self.data_input.unidade_centralizadora)
            time.sleep(2)
            list_selectors = self.page.query_selector_all(f'[title="{self.data_input.unidade_centralizadora.title()}"]')
            list_selectors[len(list_selectors)-1].dblclick()
            time.sleep(2)
            self.iframe.query_selector('[name="Fase"]').type(self.data_input.situacao)
            time.sleep(2)
            self.page.query_selector(f'[title="{self.data_input.situacao.title()}"]').dblclick()
            time.sleep(2)
            self.iframe.query_selector('[name="Nucleo"]').type(self.data_input.escritorio)
            time.sleep(4)
            list_selectors = self.page.query_selector_all(f'[title="{self.data_input.escritorio.title()}"]')
            list_selectors[len(list_selectors)-1].dblclick()
            time.sleep(2)
            self.iframe.query_selector('[name="CLI_Estrategico"]').type(self.data_input.estrategico)
            time.sleep(3)
            list_selectors_nao = self.page.query_selector_all(f'[title="{self.data_input.estrategico.title()}"]')
            list_selectors_nao[len(list_selectors_nao)-1].dblclick()
            time.sleep(2)
            if 'trabalhista' in self.data_input.natureza.lower() or 'tributario' in self.data_input.natureza.lower():
                self.iframe.query_selector('[name="CLI_DiscussaoAdm"]').fill('')
                time.sleep(3)
                self.iframe.query_selector('[name="CLI_DiscussaoAdm"]').type(self.data_input.houve_discussao_anterior)
                time.sleep(7)
                list_selectors_nao = self.page.query_selector_all(f'[title="{self.data_input.houve_discussao_anterior.title()}"]')
                list_selectors_nao[len(list_selectors_nao)-1].dblclick()
            self.iframe.query_selector('[name="CLI_EnvolveBaseMetals"]').type(self.data_input.envolve_base_metais)
            time.sleep(1)
            list_selectors_nao = self.page.query_selector_all(f'[title="{self.data_input.envolve_base_metais.title()}"]')
            list_selectors_nao[len(list_selectors_nao)-1].dblclick()
            self.iframe.query_selector('[id="bm-Save"]').click()
            time.sleep(10)
            if self.page.query_selector('[id="messagebox"]').is_visible():
                self.page.query_selector('button:has-text("OK")').click()
            self.iframe.wait_for_selector('[name="AdvogadoAdverso"]')
            time.sleep(5)
            self.iframe.query_selector('[name="AdvogadoAdverso"]').click()
            time.sleep(5)
            self.iframe.query_selector('[name="AdvogadoAdverso"]').type(self.data_input.advogado_adverso)
            time.sleep(22)
            if not self.page.query_selector(f'[title="{self.data_input.advogado_adverso.title()}"]'):
                pass
                # TO DO: ADICIONAR CADASTRO ADV ADVERSO
            self.page.query_selector(f'[title="{self.data_input.advogado_adverso.title()}"]').dblclick()
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos gerais finalizado")
            return {
                "page": self.page,
                "iframe": self.iframe
            }
        except Exception as e:
            print(str(e))
            raise Exception("Erro ao preencher os Dados Gerais")
