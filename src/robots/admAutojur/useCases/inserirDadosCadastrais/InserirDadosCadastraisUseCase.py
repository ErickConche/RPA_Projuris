import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class InserirDadosCadastraisUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        try:
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:4\\:j_idt325\\:ff\\:txt-numero-processo").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:4\\:j_idt325\\:ff\\:txt-numero-processo").type(self.data_input.numero_reclamacao)
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:5\\:j_idt325\\:ff\\:txt-localizador").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:5\\:j_idt325\\:ff\\:txt-localizador").type(self.data_input.pasta)
            time.sleep(1)
            self.page.fill('#form-dados-cadastrais\\:j_idt324\\:6\\:j_idt325\\:ff\\:cal-data-solicitacao_input',self.data_input.data_solicitacao)
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:12\\:j_idt325\\:ff\\:txt-descricao-objetos").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:12\\:j_idt325\\:ff\\:txt-descricao-objetos").type(self.data_input.observacoes)
            time.sleep(15)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:0\\:j_idt325\\:ff\\:ac-tipo-extrajudicial_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:0\\:j_idt325\\:ff\\:ac-tipo-extrajudicial_input").type(self.data_input.tipo_extrajudicial)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.tipo_extrajudicial}"]').click()
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:1\\:j_idt325\\:ff\\:ac-tipo-subpasta_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:1\\:j_idt325\\:ff\\:ac-tipo-subpasta_input").type(self.data_input.tipo_processo.upper())
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.tipo_processo.upper()}"]').click()
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:2\\:j_idt325\\:ff\\:ac-situacao_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:2\\:j_idt325\\:ff\\:ac-situacao_input").type(self.data_input.situacao.upper())
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.situacao.upper()}"]').click()
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:10\\:j_idt325\\:j_idt326\\:ff-tag\\:btn-tag-vazia").click()
            time.sleep(3)
            self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:repeat-tag\\:0\\:j_idt1151\\:2\\:j_idt1152").click()
            time.sleep(3)
            self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:repeat-tag\\:1\\:j_idt1151\\:0\\:j_idt1152").click()
            time.sleep(3)
            self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:link-salvar").click()
            time.sleep(3)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:8\\:j_idt325\\:ff\\:ac-cidade-uf_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:8\\:j_idt325\\:ff\\:ac-cidade-uf_input").type(self.data_input.uf.upper())
            time.sleep(5)
            if not self.page.locator(f'li[data-item-label="{self.data_input.uf.upper()}"]').is_visible():
                message = "Cidade não encontrada"
                self.classLogger.message(message)
                raise Exception(message)
            self.page.locator(f'li[data-item-label="{self.data_input.uf.upper()}"]').click()
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:8\\:j_idt325\\:ff\\:ac-cidade_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:8\\:j_idt325\\:ff\\:ac-cidade_input").type(self.data_input.cidade)
            time.sleep(1)
            self.page.locator(f'li[data-item-label="{self.data_input.cidade}"]').click()
            time.sleep(1)

        except Exception as error:
            message = "Erro ao inserir dados cadastrais"
            self.classLogger.message(message)
            raise Exception ("Erro ao inserir dados cadastrais")
