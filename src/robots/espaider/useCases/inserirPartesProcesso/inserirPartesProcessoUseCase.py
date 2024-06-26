from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
from unidecode import unidecode
from robots.espaider.useCases.criarPartes.criarPartesUseCase import CriarPartesUseCase
from robots.espaider.useCases.helpers.createPartHelper import criar_parte
from robots.espaider.useCases.helpers.selectOptionHelper import select_option

class InserirPartesProcessoUseCase:
    def __init__(
        self, 
        page: Page,
        frame: Frame,
        data_input: DadosEntradaEspaiderModel,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.frame = frame
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        name_inputs = [
            "Adverso",
            "ClientePatrocinador",
        ]

        de_para = {
            "Adverso":"parte_contraria",
            "ClientePatrocinador":"litisconsorte",
        }
        
        try:
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos partes do processo iniciado")
            for name in name_inputs:
                selected = False
                value = getattr(self.data_input, de_para[name])
                value = unidecode(value).lower()
                if name == 'ClientePatrocinador' and not value:
                    continue
                input = self.frame.wait_for_selector(f'[name={name}]')
                input.fill(value)

                selected = self.select_option(value=value, name=name)

                if not selected:
                    raise(f'Erro ao preencher dados, campo: {name}')
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos partes do processo finalizado")
            return
        except Exception as e:
            message = e.args[0]
            self.classLogger.message(message)
            raise e

    def select_option(self, value, name):
        select = self.frame.wait_for_selector(f'#{name}')
        if not select:
            raise(f'Erro ao preencher dados, campo: {name}')
        select.click()
        self.page.wait_for_timeout(2000)
        
        selected = select_option(page=self.page, name=name, value=value)
        if not selected and name in ['Adverso', 'ClientePatrocinador']:
            criar_parte(
                value=self.data_input.parte_contraria, 
                cpfcnpj=self.data_input.cpf_cnpj_parte_contraria, 
                page=self.page, 
                frame=self.frame, 
                data_input=self.data_input, 
                classLogger=self.classLogger
            )
            return self.select_option(value=value, name=name)
        return selected