import re
import time

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from robots.projuris.useCases.Dados_Teste import dados_teste

#from modules.downloadS3.downloadS3 import DownloadS3
from modules.logger.Logger import Logger
# from src.robots.projuris.useCases.inserir-pArquivosUseCase import InserirArquivosProjurisUseCase
from robots.projuris.useCases.LoginProjurisUseCase import LoginProjurisUseCase
from robots.projuris.useCases.CustasUseCase import CustasUseCase
from robots.projuris.useCases.GarantiasUseCase import GarantiasUseCase
from robots.projuris.useCases.QuitacoesUseCase import QuitacoesUseCase

load_dotenv()

class Projuris:
    def __init__(self):
        self.logger = Logger(hiring_id = f"process_{int(time.time())}")
        self.logger.message("Iniciando Robô Projuris")

        # Carrega os dados de teste
        for key, value in dados_teste.items():
            setattr(self, key, value)

    def execute(self):
        with sync_playwright() as p:
            # Inicializa o navegador
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Acessa a página e realiza o login no Projuris
            LoginProjurisUseCase(
                page=page,
                logger=self.logger,
                login=self.login,
                senha=self.senha
                ).execute()

            # Clica em Processos
            page.query_selector('div[tree-node-id="PR"]').click()
            time.sleep(1)
            #Clica em Todos
            page.locator("div").filter(has_text=re.compile(r"^Todos$")).click()
            time.sleep(60)
            # Preenche o campo com o numero do processo
            if page.locator("tbody.x-btn-small.x-btn-icon-small-left button.x-btn-text:has-text('OK')").is_visible():
                page.locator("tbody.x-btn-small.x-btn-icon-small-left button.x-btn-text:has-text('OK')").click()
            page.wait_for_selector("td.x-toolbar-cell div.x-form-field-wrap input.x-form-text", timeout=200000)
            time.sleep(5)
            page.locator("td.x-toolbar-cell div.x-form-field-wrap input.x-form-text").click()
            page.locator("td.x-toolbar-cell div.x-form-field-wrap input.x-form-text").fill(self.processo)
            page.keyboard.press("Enter")
            time.sleep(4)
            # Clica na Pasta do processo
            page.locator('//td[contains(@class, "x-grid3-td-")]/div[contains(@class, "x-grid3-cell-inner")]/div[contains(@class, "link-comum x-tabs-text")]').nth(1).click()
            time.sleep(3)

            if self.contexto_atividade == "Custas":
            #Custas
                try:
                    CustasUseCase(
                        page,
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
                    self.logger.message(f"Erro ao processar custas: {e}")

            elif self.contexto_atividade == "Garantias":
            #192 - Garantias
                try:
                    GarantiasUseCase(
                        page,
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
                        self.depositada_pelo,
                        self.logger
                        ).execute()
                    
                except Exception as e:
                    self.logger.message(f"Erro ao processar garantias: {e}")

            elif self.contexto_atividade == "Quitacoes":
            #Quitações
                try:
                    QuitacoesUseCase(
                        page,
                        self.parcela_quitacoes,
                        self.data_vencimento_quitacoes,
                        self.principal_quitacoes,
                        self.caso_acordo_condenacao,
                        self.sentenca_condenacao,
                        self.pago_condenacao,
                        self.tipo_pagamento_quitacoes,
                        self.item_quitacao,
                        self.situacao_quitacoes,
                        self.devido_quitacoes,
                        self.data_pagamento_quitacoes,
                        self.valor_pago_quitacoes,
                        self.logger
                        ).execute()
                    
                except Exception as e:
                    self.logger.message(f"Erro ao processar quitações: {e}")

        # 4 - DOCUMENTOS
        # Para todos os lançamentos que serão realizados no Projuris, existe a possibilidade de lançarmos documentos correspondentes às movimentações capturadas e classificadas pela Docato.
        # Ainda, acredito ser melhor definirmos os meios que são possíveis de realizar esses lançamentos de documentos, para posteriormente definir e descrever as maneiras neste documento de apoio;
        # “O dossiê que fazemos tem os dados dos depósitos e também das Liberações... seria o caso de entender se anexariamos apenas no depósito”

        # anexar_documento(page)

if __name__ == "__main__":
    robozinho = Projuris()
    robozinho.execute()