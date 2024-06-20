import time
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.judLegalone.useCases.buscarEnvolvido.buscarEnvolvidoUseCase import BuscarEnvolvidoUseCase
from robots.judLegalone.useCases.paginarElemento.paginarElementoUseCase import PaginarElementoUseCase
from robots.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirDadosEnvolvidoUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.context = context

    def execute(self):
        try:
            self.page.locator('p:has-text("Contrário principal")').click()
            time.sleep(3)
            usuario = BuscarEnvolvidoUseCase(
                nome_envolvido=self.data_input.nome_envolvido,
                cpf_cnpj_envolvido=self.data_input.cpf_cnpj_envolvido,
                classLogger=self.classLogger,
                context=self.context
            ).execute()

            nome_usuario = usuario.get("Text") if usuario.get("Text") else usuario.get("Value")

            self.page.locator("#Contrario_EnvolvidoText").click()
            time.sleep(1)
            self.page.locator("#Contrario_EnvolvidoText").type(nome_usuario)
            time.sleep(3)
            self.page.locator("#Contrario_EnvolvidoText").press("Enter")
            time.sleep(3)
            elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
            PaginarElementoUseCase(
                page=self.page,
                classLogger=self.classLogger,
                context=self.context,
                id_elemento=usuario.get("Id"),
                valor_elemento=nome_usuario,
                data_val_field='ContatoNome'
            ).execute()
            elemento_dropdown.locator(f'tr[data-val-id="{usuario.get("Id")}"] td[data-val-field="ContatoNome"]:text("{nome_usuario}")').click()
            time.sleep(2)
        except Exception as error:
            raise Exception("Erro ao inserir os dados dos envolvidos")