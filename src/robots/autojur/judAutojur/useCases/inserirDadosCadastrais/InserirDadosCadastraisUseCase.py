import time
from unidecode import unidecode
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from modules.deparaGeral.deparaGeral import DeparaGeral
from robots.autojur.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel
from robots.autojur.judAutojur.useCases.verificarDuplicidadeLitispendencia.verificarDuplicidadeLitispendenciaUseCase import VerificarDuplicidadeLitispendenciaUseCase

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
        self.depara = DeparaGeral()

    def execute(self):
        try:
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:0\\:j_idt325\\:ff\\:txt-cnj").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:0\\:j_idt325\\:ff\\:txt-cnj").type(self.data_input.processo)
            time.sleep(2)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:1\\:j_idt325\\:ff\\:txt-numero-processo").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:1\\:j_idt325\\:ff\\:txt-numero-processo").type(self.data_input.processo)
            time.sleep(2)

            if self.page.locator("#modal-duplicados").is_visible():
                VerificarDuplicidadeLitispendenciaUseCase(
                    page=self.page,
                    data_input=self.data_input,
                    classLogger=self.classLogger,
                    tag="#modal-duplicados"
                ).execute()

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:28\\:j_idt325\\:ff\\:txt-numero-processo-originario").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:28\\:j_idt325\\:ff\\:txt-numero-processo-originario").type(self.data_input.processo_originario)
            time.sleep(2)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:3\\:j_idt325\\:ff\\:txt-localizador").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:3\\:j_idt325\\:ff\\:txt-localizador").type(self.data_input.pasta)
            time.sleep(2)

            self.page.fill('#form-dados-cadastrais\\:j_idt324\\:21\\:j_idt325\\:ff\\:cal-data-acao_input',self.data_input.data_distribuicao)
            time.sleep(2)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:5\\:j_idt325\\:ff\\:ac-tipo-acao_input").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:5\\:j_idt325\\:ff\\:ac-tipo-acao_input").type(self.data_input.titulo)
            time.sleep(2)
            if self.data_input.titulo == 'Cumprimento de Sentença':
                self.page.locator(f'li[data-item-label="{self.data_input.titulo}"]').click()
                time.sleep(3)
            else:
                self.page.locator(f'li[data-item-label="{unidecode(self.data_input.titulo)}"]').click()
                time.sleep(3)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:7\\:j_idt325\\:ff\\:ac-fase_input").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:7\\:j_idt325\\:ff\\:ac-fase_input").type(self.data_input.fase)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.fase}"]').click()
            time.sleep(2)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:6\\:j_idt325\\:ff\\:ac-natureza_input").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:6\\:j_idt325\\:ff\\:ac-natureza_input").type(self.data_input.natureza)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.natureza}"]').click()
            time.sleep(2)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:19\\:j_idt325\\:ff\\:ac-situacao_input").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:19\\:j_idt325\\:ff\\:ac-situacao_input").type(self.data_input.situacao)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.situacao}"]').click()
            time.sleep(2)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:13\\:j_idt325\\:ff\\:ac-juizo-uf_input").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:13\\:j_idt325\\:ff\\:ac-juizo-uf_input").type(self.data_input.uf)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.uf}"]').click()
            time.sleep(2)
            
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:13\\:j_idt325\\:ff\\:ac-juizo_input").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:13\\:j_idt325\\:ff\\:ac-juizo_input").type(self.data_input.cidade.upper())
            time.sleep(2)
            if self.page.locator(f'li[data-item-label="{self.data_input.cidade.upper()}"]').is_visible():
                self.page.locator(f'li[data-item-label="{self.data_input.cidade.upper()}"]').click()
                time.sleep(3)

            elif self.page.locator(f'li[data-item-label="{unidecode(self.data_input.cidade.upper())}"]').is_visible():
                self.page.locator(f'li[data-item-label="{unidecode(self.data_input.cidade.upper())}"]').click()
                time.sleep(3)

            elif self.page.locator(f'li[data-item-label="{self.data_input.cidade}"]').is_visible():
                self.page.locator(f'li[data-item-label="{self.data_input.cidade}"]').click()
                time.sleep(3)

            else:
                capital = unidecode(self.depara.depara_estado_capital(self.data_input.uf)).upper()
                self.page.locator("#form-dados-cadastrais\\:j_idt324\\:13\\:j_idt325\\:ff\\:ac-juizo_input").clear()
                time.sleep(2)
                self.page.locator("#form-dados-cadastrais\\:j_idt324\\:13\\:j_idt325\\:ff\\:ac-juizo_input").type(capital.upper())
                time.sleep(2)
                self.page.locator(f'li[data-item-label="{capital.upper()}"]').click()

            if self.page.locator("#modal-litispendencia").is_visible():
                VerificarDuplicidadeLitispendenciaUseCase(
                    page=self.page,
                    data_input=self.data_input,
                    classLogger=self.classLogger,
                    tag="#modal-litispendencia"
                ).execute()
            attemp = 0
            max_attemp = 3
            while attemp < max_attemp:
                attemp += 1
                self.page.locator("#form-dados-cadastrais\\:j_idt324\\:32\\:j_idt325\\:j_idt326\\:ff-tag\\:btn-tag-vazia").click()
                time.sleep(5)
                if self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:repeat-tag\\:0\\:j_idt1153\\:2\\:j_idt1154").is_visible():
                    attemp = max_attemp
            self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:repeat-tag\\:0\\:j_idt1153\\:2\\:j_idt1154").click()
            time.sleep(5)
            self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:repeat-tag\\:2\\:j_idt1153\\:1\\:j_idt1154").click()
            time.sleep(5)
            self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:link-salvar").click()
            time.sleep(5)
            
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:10\\:j_idt325\\:ff\\:ac-orgao-julgador_input").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:10\\:j_idt325\\:ff\\:ac-orgao-julgador_input").type(self.data_input.orgao_julgador)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{unidecode(self.data_input.orgao_julgador.replace("-"," ").upper())}"]').click()
            time.sleep(2)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:16\\:j_idt325\\:ff\\:ac-rito_input").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:16\\:j_idt325\\:ff\\:ac-rito_input").type(self.data_input.rito)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.rito}"]').click()
            time.sleep(2)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:20\\:j_idt325\\:ff\\:ac-sistema-tribunal_input").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:20\\:j_idt325\\:ff\\:ac-sistema-tribunal_input").type(self.data_input.sistema_tribunal)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.sistema_tribunal}"]').click()
            time.sleep(2)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:4\\:j_idt325\\:ff\\:txt-descricao-objetos").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:4\\:j_idt325\\:ff\\:txt-descricao-objetos").type(self.data_input.descricao_objeto)
            time.sleep(2)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:15\\:j_idt325\\:ff\\:ac-competencia_input").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:15\\:j_idt325\\:ff\\:ac-competencia_input").type(self.data_input.competencia)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.competencia}"]').click()
            time.sleep(2)

            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:9\\:j_idt325\\:ff\\:ac-portfolio_input").click()
            time.sleep(2)
            self.page.locator("#form-dados-cadastrais\\:j_idt324\\:9\\:j_idt325\\:ff\\:ac-portfolio_input").type(self.data_input.portfolio)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.portfolio}"]').click()
            time.sleep(2)

        except Exception as error:
            message = "Erro ao inserir dados cadastrais"
            self.classLogger.message(message)
            raise Exception ("Erro ao inserir dados cadastrais")