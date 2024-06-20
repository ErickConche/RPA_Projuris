import time
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.admLegalone.useCases.deparas.deparas import Deparas
from robots.legalone.useCases.buscarEnvolvido.buscarEnvolvidoUseCase import BuscarEnvolvidoUseCase

class InserirDadosEnvolvidosUseCase:
    def __init__(
        self,
        page: Page,
        nome_envolvido:str,
        cpf_cnpj_envolvido: str,
        tipo_envolvido:str,
        posicao_envolvido: str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.page = page
        self.nome_envolvido = nome_envolvido
        self.cpf_cnpj_envolvido = cpf_cnpj_envolvido
        self.tipo_envolvido = tipo_envolvido
        self.posicao_envolvido = posicao_envolvido
        self.classLogger = classLogger
        self.context = context

    def execute(self):
        try:
            self.page.query_selector(f'#add_outroEnvolvido').click()
            time.sleep(3)
            usuario = BuscarEnvolvidoUseCase(
                nome_envolvido=self.nome_envolvido,
                cpf_cnpj_envolvido=self.cpf_cnpj_envolvido,
                classLogger=self.classLogger,
                context=self.context
            ).execute()
            
            elemento_envolvido = self.page.locator('[id^="OutrosEnvolvidos_"][id$="__PosicaoEnvolvidoText"]')
            id_do_cliente_envolvido = elemento_envolvido.get_attribute('id').replace("OutrosEnvolvidos_","").replace("__PosicaoEnvolvidoText","")
            self.page.query_selector(f'#OutrosEnvolvidos_{id_do_cliente_envolvido}__PosicaoEnvolvidoText').click()
            time.sleep(1)
            self.page.query_selector(f'#OutrosEnvolvidos_{id_do_cliente_envolvido}__PosicaoEnvolvidoText').type(self.posicao_envolvido)
            time.sleep(1)
            elemento_envolvido = self.page.locator(f'#OutrosEnvolvidos_{id_do_cliente_envolvido}__LookupPosicaoNaoUnica')
            elemento_envolvido.locator('.lookup-button.lookup-filter').click()
            time.sleep(5)
            self.page.locator(f'tr[data-val-id="{Deparas.depara_posicao_reclamante(self.posicao_envolvido)}"]').click() ### Criar depara
            time.sleep(3)

            self.page.query_selector(f'#OutrosEnvolvidos_{id_do_cliente_envolvido}__EnvolvidoText').click()
            time.sleep(1)
            self.page.query_selector(f'#OutrosEnvolvidos_{id_do_cliente_envolvido}__EnvolvidoText').type(self.nome_envolvido)
            time.sleep(1)
            elemento_envolvido = self.page.locator(f'#OutrosEnvolvidos_{id_do_cliente_envolvido}__LookupContato')
            elemento_envolvido.locator('.lookup-button.lookup-filter').click()
            time.sleep(5)
            self.page.locator(f'tr[data-val-id="{usuario.get("Id")}"]').click() 
            time.sleep(3)

        except Exception as error:
            raise Exception("Erro ao inserir dados dos envolvidos no formulario de criação")
        