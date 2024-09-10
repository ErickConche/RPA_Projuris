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
            id_txt_cnj = self.page.query_selector('label:has-text("CNJ *")').get_attribute('for')
            id_txt_cnj = id_txt_cnj.replace(':', '\\:').replace('localizador', 'cnj')
            self.page.query_selector(f"#{id_txt_cnj}").click()
            time.sleep(2)
            self.page.query_selector(f"#{id_txt_cnj}").type(self.data_input.processo)
            time.sleep(2)

            id_txt_num_processo = self.page.query_selector('label:has-text("Processo *")').get_attribute('for')
            id_txt_num_processo = id_txt_num_processo.replace(':', '\\:').replace('localizador', 'numero-processo')
            self.page.query_selector(f"#{id_txt_num_processo}").click()
            time.sleep(2)
            self.page.query_selector(f"#{id_txt_num_processo}").type(self.data_input.processo)
            time.sleep(2)

            if self.page.locator("#modal-duplicados").is_visible():
                VerificarDuplicidadeLitispendenciaUseCase(
                    page=self.page,
                    data_input=self.data_input,
                    classLogger=self.classLogger,
                    tag="#modal-duplicados"
                ).execute()

            id_txt_num_processo_origin = self.page.query_selector('label:has-text("Número Processo Originário *")').get_attribute('for')
            id_txt_num_processo_origin = id_txt_num_processo_origin.replace(':', '\\:').replace('localizador', 'numero-processo-originario')
            self.page.query_selector(f"#{id_txt_num_processo_origin}").click()
            time.sleep(2)
            self.page.query_selector(f"#{id_txt_num_processo_origin}").type(self.data_input.processo_originario)
            time.sleep(2)

            id_txt_localizador = self.page.query_selector('label:has-text("Localizador")').get_attribute('for')
            id_txt_localizador = id_txt_localizador.replace(':', '\\:')
            self.page.query_selector(f"#{id_txt_localizador}").click()
            time.sleep(2)
            self.page.query_selector(f"#{id_txt_localizador}").type(self.data_input.pasta)
            time.sleep(2)

            id_txt_data_acao = self.page.query_selector('label:has-text("Data Ação *")').get_attribute('for')
            id_txt_data_acao = id_txt_data_acao.replace(':', '\\:').replace('txt-localizador', 'cal-data-acao_input')
            self.page.fill(f'#{id_txt_data_acao}', self.data_input.data_distribuicao)
            time.sleep(2)

            id_txt_tipo_acao = self.page.query_selector('label:has-text("Tipo de Ação *")').get_attribute('for')
            id_txt_tipo_acao = id_txt_tipo_acao.replace(':', '\\:').replace('txt-localizador', 'ac-tipo-acao_input')
            self.page.locator(f"#{id_txt_tipo_acao}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_tipo_acao}").type(self.data_input.titulo)
            time.sleep(2)
            if self.data_input.titulo == 'Cumprimento de Sentença':
                self.page.locator(f'li[data-item-label="{self.data_input.titulo}"]').click()
                time.sleep(3)
            else:
                self.page.locator(f'li[data-item-label="{unidecode(self.data_input.titulo)}"]').click()
                time.sleep(3)

            id_txt_fase = self.page.query_selector('label:has-text("Fase Processual *")').get_attribute('for')
            id_txt_fase = id_txt_fase.replace(':', '\\:').replace('txt-localizador', 'ac-fase_input')
            self.page.locator(f"#{id_txt_fase}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_fase}").type(self.data_input.fase)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.fase}"]').click()
            time.sleep(2)

            id_txt_natureza = self.page.query_selector('label:has-text("Natureza *")').get_attribute('for')
            id_txt_natureza = id_txt_natureza.replace(':', '\\:').replace('txt-localizador', 'ac-natureza_input')
            self.page.locator(f"#{id_txt_natureza}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_natureza}").type(self.data_input.natureza)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.natureza}"]').click()
            time.sleep(2)

            id_txt_situacao = self.page.query_selector('label:has-text("Situação *")').get_attribute('for')
            id_txt_situacao = id_txt_situacao.replace(':', '\\:').replace('txt-localizador', 'ac-situacao_input')
            self.page.locator(f"#{id_txt_situacao}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_situacao}").type(self.data_input.situacao)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.situacao}"]').click()
            time.sleep(2)

            id_txt_juizo = self.page.query_selector('label:has-text("Juízo *")').get_attribute('for')
            id_txt_juizo_uf = id_txt_juizo.replace(':', '\\:').replace('txt-localizador', 'ac-juizo-uf_input')
            id_txt_juizo = id_txt_juizo.replace(':', '\\:').replace('txt-localizador', 'ac-juizo_input')
            self.page.locator(f"#{id_txt_juizo_uf}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_juizo_uf}").type(self.data_input.uf)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.uf}"]').click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_juizo}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_juizo}").type(self.data_input.cidade.upper())
            time.sleep(2)
            if self.page.locator(f'li[data-item-label="{self.data_input.cidade.upper()}"]').is_visible():
                self.page.locator(f'li[data-item-label="{self.data_input.cidade.upper()}"]').click()
                time.sleep(3)

            elif self.page.locator(f'li[data-item-label="{unidecode(self.data_input.cidade.upper())}"]').is_visible():
                self.page.locator(f'li[data-item-label="{unidecode(self.data_input.cidade.upper())}"]').click()
                time.sleep(3)

            elif self.page.locator(f'li[data-item-label="{unidecode(self.data_input.cidade.upper())}"]').is_visible():
                self.page.locator(f'li[data-item-label="{self.data_input.cidade}"]').click()
                time.sleep(3)

            else:
                capital = unidecode(self.depara.depara_estado_capital(self.data_input.uf)).upper()
                self.page.locator(f"#{id_txt_juizo}").clear()
                time.sleep(2)
                self.page.locator(f"#{id_txt_juizo}").type(capital.upper())
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
                id_btn_tags = self.page.query_selector('label:has-text("Tags de Controle")').get_attribute('id')
                id_btn_tags = id_btn_tags.replace(':', '\\:').replace('_label', '\\:btn-tag-vazia')
                self.page.locator(f"#{id_btn_tags}").click()
                time.sleep(5)
                if self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:repeat-tag\\:0\\:linha").is_visible():
                    attemp = max_attemp
            self.page.locator('a[aria-label="ESCRITÓRIO"]').click()
            time.sleep(10)
            self.page.locator('a[aria-label="SP"]').click()
            time.sleep(5)
            self.page.locator("#modal-tags-processo\\:form-cad-tag-controle\\:link-salvar").click()
            time.sleep(5)

            id_txt_orgao_julgador = self.page.query_selector('label:has-text("Órgão Julgador *")').get_attribute('for')
            id_txt_orgao_julgador = id_txt_orgao_julgador.replace(':', '\\:').replace('txt-localizador', 'ac-orgao-julgador_input')
            self.page.locator(f"#{id_txt_orgao_julgador}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_orgao_julgador}").type(self.data_input.orgao_julgador)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{unidecode(self.data_input.orgao_julgador.replace("-"," ").upper())}"]').click()
            time.sleep(2)

            id_txt_rito = self.page.query_selector('label:has-text("Rito *")').get_attribute('for')
            id_txt_rito = id_txt_rito.replace(':', '\\:').replace('txt-localizador', 'ac-rito_input')
            self.page.locator(f"#{id_txt_rito}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_rito}").type(self.data_input.rito)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.rito}"]').click()
            time.sleep(2)

            id_txt_sistema_tributario = self.page.query_selector('label:has-text("Sistema Tribunal *")').get_attribute('for')
            id_txt_sistema_tributario = id_txt_sistema_tributario.replace(':', '\\:').replace('txt-localizador', 'ac-sistema-tribunal_input')
            self.page.locator(f"#{id_txt_sistema_tributario}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_sistema_tributario}").type(self.data_input.sistema_tribunal)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.sistema_tribunal}"]').click()
            time.sleep(2)

            id_txt_descricao_obj = self.page.query_selector('label:has-text("Descrição dos Objetos *")').get_attribute('for')
            id_txt_descricao_obj = id_txt_descricao_obj.replace(':', '\\:').replace('localizador', 'descricao-objetos')
            self.page.locator(f"#{id_txt_descricao_obj}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_descricao_obj}").type(self.data_input.descricao_objeto)
            time.sleep(2)

            id_txt_competencia = self.page.query_selector('label:has-text("Competência *")').get_attribute('for')
            id_txt_competencia = id_txt_competencia.replace(':', '\\:').replace('txt-localizador', 'ac-competencia_input')
            self.page.locator(f"#{id_txt_competencia}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_competencia}").type(self.data_input.competencia)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.competencia}"]').click()
            time.sleep(2)

            id_txt_portfolio = self.page.query_selector('label:has-text("Portfólio *")').get_attribute('for')
            id_txt_portfolio = id_txt_portfolio.replace(':', '\\:').replace('txt-localizador', 'ac-portfolio_input')
            self.page.locator(f"#{id_txt_portfolio}").click()
            time.sleep(2)
            self.page.locator(f"#{id_txt_portfolio}").type(self.data_input.portfolio)
            time.sleep(2)
            self.page.locator(f'li[data-item-label="{self.data_input.portfolio}"]').click()
            time.sleep(2)

        except Exception as error:
            message = "Erro ao inserir dados cadastrais"
            print(message + ' ' + error)
            self.classLogger.message(message)
            raise Exception("Erro ao inserir dados cadastrais")
