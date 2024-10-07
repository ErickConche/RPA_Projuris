import time
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class InserirDadosPersonalizadosUseCase:
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
            id_nome_orgao_adm = self.page.query_selector('label:has-text("Nome Órgão Administrativo")').get_attribute('id')
            parts = id_nome_orgao_adm.split(":")
            parts[-1] = "cp-texto--"
            id_nome_orgao_adm = ":".join(parts)
            id_nome_orgao_adm = id_nome_orgao_adm.replace(':', '\\:')
            self.page.locator(f"#{id_nome_orgao_adm}").click()
            time.sleep(1)
            self.page.locator(f"#{id_nome_orgao_adm}").type(self.data_input.nome_procon)
            time.sleep(1)
            id_dados_reserva = self.page.query_selector('label:has-text("Demais Dados Reserva")').get_attribute('id')
            parts = id_dados_reserva.split(":")
            parts[-1] = "cp-texto--"
            id_dados_reserva = ":".join(parts)
            id_dados_reserva = id_dados_reserva.replace(':', '\\:')
            self.page.locator(f"#{id_dados_reserva}").click()
            time.sleep(1)
            self.page.locator(f"#{id_dados_reserva}").type(self.data_input.dados_reserva)
            time.sleep(1)
            id_tipo_reclamacao = self.page.query_selector('label:has-text("Tipo da Reclamação")').get_attribute('id')
            parts = id_tipo_reclamacao.split(":")
            parts[-1] = "cp-list--"
            id_tipo_reclamacao = ":".join(parts)
            id_tipo_reclamacao = id_tipo_reclamacao.replace(':', '\\:')
            self.page.locator(f'button[data-id="{id_tipo_reclamacao}"]').click()
            time.sleep(3)
            self.page.locator('li:has-text("Digital")').click()
            time.sleep(3)
        except Exception as error:
            message = "Erro ao inserir dados personalizados"
            self.classLogger.message(message)
            raise Exception ("Erro ao inserir dados personalizados")