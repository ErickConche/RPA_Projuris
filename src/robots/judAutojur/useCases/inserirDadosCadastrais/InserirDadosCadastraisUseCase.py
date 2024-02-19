import time
from unidecode import unidecode
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

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
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:0\\:j_idt325\\:ff\\:txt-cnj").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:0\\:j_idt325\\:ff\\:txt-cnj").type(self.data_input.processo)
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:1\\:j_idt325\\:ff\\:txt-numero-processo").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:1\\:j_idt325\\:ff\\:txt-numero-processo").type(self.data_input.processo)
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:28\\:j_idt325\\:ff\\:txt-numero-processo-originario").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:28\\:j_idt325\\:ff\\:txt-numero-processo-originario").type(self.data_input.processo_originario)
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:3\\:j_idt325\\:ff\\:txt-localizador").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:3\\:j_idt325\\:ff\\:txt-localizador").type(self.data_input.pasta)
            time.sleep(1)

            self.page.fill('#form-dados-cadastrais\\:j_idt324\\:21\\:j_idt325\\:ff\\:cal-data-acao_input',self.data_input.data_distribuicao)
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:5\\:j_idt325\\:ff\\:ac-tipo-acao_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:5\\:j_idt325\\:ff\\:ac-tipo-acao_input").type(self.data_input.titulo)
            time.sleep(2)
            if self.data_input.titulo == 'Cumprimento de Sentença':
                self.page.locator(f'li[data-item-label="{self.data_input.titulo}"]').click()
                time.sleep(1)
            else:
                self.page.locator(f'li[data-item-label="{unidecode(self.data_input.titulo)}"]').click()
                time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:7\\:j_idt325\\:ff\\:ac-fase_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:7\\:j_idt325\\:ff\\:ac-fase_input").type(self.data_input.fase)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.fase}"]').click()
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:6\\:j_idt325\\:ff\\:ac-natureza_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:6\\:j_idt325\\:ff\\:ac-natureza_input").type(self.data_input.natureza)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.natureza}"]').click()
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:19\\:j_idt325\\:ff\\:ac-situacao_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:19\\:j_idt325\\:ff\\:ac-situacao_input").type(self.data_input.situacao)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.situacao}"]').click()
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:13\\:j_idt325\\:ff\\:ac-juizo-uf_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:13\\:j_idt325\\:ff\\:ac-juizo-uf_input").type(self.data_input.uf)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.uf}"]').click()
            time.sleep(1)
            
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:13\\:j_idt325\\:ff\\:ac-juizo_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:13\\:j_idt325\\:ff\\:ac-juizo_input").type(self.data_input.cidade.upper())
            time.sleep(2)
            if self.page.locator(f'li[data-item-label="{self.data_input.cidade.upper()}"]').is_visible():
                self.page.locator(f'li[data-item-label="{self.data_input.cidade.upper()}"]').click()
                time.sleep(1)

            if self.page.locator(f'li[data-item-label="{unidecode(self.data_input.cidade.upper())}"]').is_visible():
                self.page.locator(f'li[data-item-label="{unidecode(self.data_input.cidade.upper())}"]').click()
                time.sleep(1)

            if self.page.locator(f'li[data-item-label="{self.data_input.cidade}"]').is_visible():
                self.page.locator(f'li[data-item-label="{self.data_input.cidade}"]').click()
                time.sleep(1)

            attemp = 0
            max_attemp = 3
            while attemp < max_attemp:
                attemp += 1
                self.page.locator("#form-dados-cadastrais\\:j_idt324\\:32\\:j_idt325\\:j_idt326\\:ff-tag\\:btn-tag-vazia").click()
                time.sleep(3)
                if self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:repeat-tag\\:0\\:j_idt1151\\:2\\:j_idt1152").is_visible():
                    attemp = max_attemp
            self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:repeat-tag\\:0\\:j_idt1151\\:2\\:j_idt1152").click()
            time.sleep(3)
            self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:repeat-tag\\:1\\:j_idt1151\\:0\\:j_idt1152").click()
            time.sleep(3)
            self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:link-salvar").click()
            time.sleep(3)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:10\\:j_idt325\\:ff\\:ac-orgao-julgador_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:10\\:j_idt325\\:ff\\:ac-orgao-julgador_input").type(self.data_input.orgao_julgador)
            time.sleep(1)
            self.page.locator(f'li[data-item-label="{unidecode(self.data_input.orgao_julgador.upper())}"]').click()
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:16\\:j_idt325\\:ff\\:ac-rito_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:16\\:j_idt325\\:ff\\:ac-rito_input").type(self.data_input.rito)
            time.sleep(1)
            self.page.locator(f'li[data-item-label="{self.data_input.rito}"]').click()
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:20\\:j_idt325\\:ff\\:ac-sistema-tribunal_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:20\\:j_idt325\\:ff\\:ac-sistema-tribunal_input").type(self.data_input.sistema_tribunal)
            time.sleep(1)
            self.page.locator(f'li[data-item-label="{self.data_input.sistema_tribunal}"]').click()
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:4\\:j_idt325\\:ff\\:txt-descricao-objetos").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:4\\:j_idt325\\:ff\\:txt-descricao-objetos").type(self.data_input.descricao_objeto)
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:15\\:j_idt325\\:ff\\:ac-competencia_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:15\\:j_idt325\\:ff\\:ac-competencia_input").type(self.data_input.competencia)
            time.sleep(1)
            self.page.locator(f'li[data-item-label="{self.data_input.competencia}"]').click()
            time.sleep(1)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:9\\:j_idt325\\:ff\\:ac-portfolio_input").click()
            time.sleep(1)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:9\\:j_idt325\\:ff\\:ac-portfolio_input").type(self.data_input.portfolio)
            time.sleep(1)
            self.page.locator(f'li[data-item-label="{self.data_input.portfolio}"]').click()
            time.sleep(1)




        except Exception as error:
            message = "Erro ao inserir dados cadastrais"
            self.classLogger.message(message)
            raise Exception ("Erro ao inserir dados cadastrais")
