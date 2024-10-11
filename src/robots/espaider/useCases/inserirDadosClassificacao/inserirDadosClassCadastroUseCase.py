import time
from modules.logger.Logger import Logger
from playwright.sync_api import Frame, Page
from robots.espaider.useCases.helpers.selectOptionHelper import select_option, select_single
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderCadastroModel import (
    DadosEntradaEspaiderCadastroModel)
from robots.espaider.useCases.helpers.createPartHelper import criar_parte


class InserirDadosClassCadastroUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderCadastroModel,
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
            self.iframe.query_selector('[name="CLI_AcaoEspecial"]').type(self.data_input.acao_especial)
            time.sleep(3)
            select_single(page=self.page, value=self.data_input.acao_especial)
            self.iframe.query_selector('[name="Cliente"]').type(self.data_input.documento_cliente_principal)
            time.sleep(15)
            if not select_option(page=self.page, name="Cliente", value=self.data_input.cliente_principal):
                raise Exception("Cliente principal não encontrado")
            time.sleep(3)
            self.iframe.wait_for_selector('[name="CondicaoCliente"]')
            self.iframe.query_selector('[name="CondicaoCliente"]').type(self.data_input.condicao_cliente)
            time.sleep(3)
            select_option(page=self.page, name="CondicaoCliente", value=self.data_input.condicao_cliente)
            time.sleep(2)
            self.iframe.query_selector('[name="CLI_NumeroProcesso"]').type(self.data_input.numero_do_processo)
            time.sleep(2)
            self.iframe.query_selector('[name="Adverso"]').type(self.data_input.documento_adverso_principal)
            time.sleep(15)
            if not select_option(page=self.page, name="Adverso", value=self.data_input.documento_adverso_principal, index=1):
                criar_parte(page=self.page, frame=self.iframe, data_input=self.data_input, classLogger=self.classLogger, value=self.data_input.adverso_principal, cpfcnpj=self.data_input.documento_adverso_principal)
                self.iframe.query_selector('[name="Adverso"]').fill("")
                self.iframe.query_selector('[name="Adverso"]').type(self.data_input.documento_adverso_principal)
                time.sleep(15)
                if not select_option(page=self.page, name="Adverso", value=self.data_input.documento_adverso_principal, index=1):
                    raise Exception("Erro ao criar Adverso / Adverso não encontrado")
            time.sleep(2)
            self.iframe.query_selector('[name="CondicaoAdverso"]').type(self.data_input.condição_adverso)
            time.sleep(2)
            self.iframe.query_selector('[name="Advogado"]').type(self.data_input.advogado_interno_vale)
            time.sleep(5)
            if not select_option(page=self.page, name="Advogado", value=self.data_input.advogado_interno_vale):
                raise Exception("Advogado não encontrado")
            time.sleep(5)
            self.iframe.query_selector('[id="RegistroNivel1Edt"]').type(self.data_input.unidade_controle)
            time.sleep(5)
            if not select_option(page=self.page, name="RegistroNivel1Edt", value=self.data_input.unidade_controle):
                raise Exception("Unidade de controle não localizado.")
            time.sleep(1)
            self.iframe.query_selector('[name="Categoria"]').type(self.data_input.natureza)
            time.sleep(5)
            select_option(page=self.page, name="Categoria", value=self.data_input.natureza)
            time.sleep(5)
            if 'trabalhista' in self.data_input.natureza.lower():
                self.iframe.query_selector('[name="CLI_TipoNatureza"]').type(self.data_input.tipo)
                time.sleep(4)
                if not select_option(page=self.page, name="CLI_TipoNatureza", value=self.data_input.tipo):
                    raise Exception(f"Tipo não encontrado:, {self.data_input.tipo}")
                time.sleep(5)
            self.iframe.query_selector('[name="Tipo"]').type(self.data_input.tipo_acao.split('  ')[0])
            time.sleep(2)
            if not select_option(page=self.page, name="Tipo", value=self.data_input.tipo_acao):
                raise Exception("Erro: Tipo ação não encontrado")
            time.sleep(2)
            self.iframe.query_selector('[name="Unidade"]').type(self.data_input.unidade_centralizadora)
            time.sleep(2)
            select_option(page=self.page, name="Unidade", value=self.data_input.unidade_centralizadora)
            time.sleep(2)
            self.iframe.query_selector('[name="Fase"]').type(self.data_input.situacao)
            time.sleep(2)
            select_option(page=self.page, name="Fase", value=self.data_input.situacao)
            time.sleep(2)
            self.iframe.query_selector('[name="Nucleo"]').type(self.data_input.escritorio)
            time.sleep(4)
            select_option(page=self.page, name="Nucleo", value=self.data_input.escritorio)
            time.sleep(2)
            self.iframe.query_selector('[name="CLI_Estrategico"]').type(self.data_input.estrategico)
            time.sleep(3)
            select_single(page=self.page, value=self.data_input.estrategico)
            time.sleep(2)
            if 'trabalhista' in self.data_input.natureza.lower() or 'tributario' in self.data_input.natureza.lower():
                self.iframe.query_selector('[name="CLI_DiscussaoAdm"]').fill(self.data_input.houve_discussao_anterior)
                time.sleep(2)
                self.iframe.query_selector('[name="CLI_DiscussaoAdm"]').click()
                time.sleep(2)
                select_single(page=self.page, value=self.data_input.houve_discussao_anterior)
            self.iframe.query_selector('[name="CLI_EnvolveBaseMetals"]').type(self.data_input.envolve_base_metais)
            time.sleep(1)
            select_single(page=self.page, value=self.data_input.envolve_base_metais)
            time.sleep(10)
            self.iframe.query_selector('[id=bm-Save]').click()
            time.sleep(5)
            if self.page.query_selector('[id="messagebox"]') and self.page.query_selector('[id="messagebox"]').is_visible():
                self.page.query_selector('button:has-text("OK")').click()
            time.sleep(20)
            self.iframe.wait_for_selector('[name="AdvogadoAdverso"]')
            adv_adverson = f'{self.data_input.advogado_adverso} - {self.data_input.documento_advogado_adverso}' if 'oab' in self.data_input.documento_advogado_adverso.lower() else self.data_input.advogado_adverso
            self.iframe.query_selector('[name="AdvogadoAdverso"]').type(adv_adverson)
            time.sleep(15)
            if not select_option(page=self.page, name="AdvogadoAdverso", value=adv_adverson):
                criar_parte(page=self.page, frame=self.iframe, data_input=self.data_input, classLogger=self.classLogger, value=adv_adverson, cpfcnpj=self.data_input.documento_advogado_adverso)
                self.iframe.query_selector('[name="AdvogadoAdverso"]').fill("")
                self.iframe.query_selector('[name="AdvogadoAdverso"]').type(adv_adverson)
                time.sleep(15)
                if not select_option(page=self.page, name="AdvogadoAdverso", value=adv_adverson):
                    raise Exception("Erro ao criar Advogado Adverso / Advogado Adverso não encontrado")
            self.iframe.query_selector('[id=bm-Save]').click()
            time.sleep(5)
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos gerais finalizado")
            return {
                "page": self.page,
                "iframe": self.iframe
            }
        except Exception as e:
            self.classLogger.message(str(e))
            raise Exception("Erro ao preencher os Dados Gerais")
