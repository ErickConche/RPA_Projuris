import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.admLegalone.useCases.percorrerPastas.percorrerPastasUseCase import PercorrerPastasUseCase
from robots.admLegalone.useCases.validarPasta.__model__.PastaModel import PastaModel

class ValidarPastaUseCase:
    def __init__(
        self,
        page: Page,
        nome_envolvido:str, 
        numero_reclamacao:str,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.nome_envolvido = nome_envolvido
        self.numero_reclamacao = numero_reclamacao
        self.classLogger = classLogger

    def execute(self)->PastaModel:
        try:
            message = "Iniciando processo de verificação se a pasta já existe para o protocolo do envolvido"
            self.classLogger.message(message)
            self.page.query_selector('#menuservicos').click()
            time.sleep(15)
            self.page.query_selector('#Search').click()
            time.sleep(10)
            self.page.query_selector('#Search').type(self.nome_envolvido)
            time.sleep(10)
            self.page.query_selector('#search-box-input-submit').click()
            time.sleep(10)
            qtde_pastas = self.page.query_selector('[class="legalone-grid-counter result-header"]').inner_text().split("Pastas de consultivo encontradas: ")[1]
            if int(qtde_pastas)<=0:
                message = "Não existe pasta para o protocolo do envolvido"
                self.classLogger.message(message)
                data_pasta: PastaModel = PastaModel(
                    found=False,
                    pasta=None,
                    data_cadastro=None,
                    url_pasta=None
                )
                return data_pasta
            else:
                return PercorrerPastasUseCase(
                    page=self.page,
                    nome_envolvido=self.nome_envolvido,
                    numero_reclamacao=self.numero_reclamacao,
                    classLogger=self.classLogger
                ).execute()
            
        except Exception as error:
            raise Exception("Erro ao validar se a pasta já existe")