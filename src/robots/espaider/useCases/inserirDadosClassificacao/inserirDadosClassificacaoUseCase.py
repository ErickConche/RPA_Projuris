from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
from unidecode import unidecode
from robots.espaider.useCases.helpers.selectOptionHelper import select_option, select_single
from robots.espaider.useCases.helpers.insertValueHelper import insert_value

class InserirDadosClassificacaoUseCase:
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
            "Fase", 
            "Natureza", 
            "Categoria", 
            "Tipo", 
            "Assunto", 
            "CLI_Contingencia"
        ]

        de_para = {
            "Fase":"fase",
            "Natureza":"natureza", 
            "Categoria":"categoria", 
            "Tipo":"tipo_acao", 
            "Assunto":"assunto", 
            "CLI_Contingencia":"contingencia"
        }

        try:
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos gerais iniciado")
            for name in name_inputs:
                value = insert_value(data_input=self.data_input, de_para=de_para, name=name, frame=self.frame)
                select = self.frame.wait_for_selector(f'#{name}')
                if not select:
                    raise(f'Erro ao preencher dados, campo: {name}')
                select.click()
                self.frame.wait_for_timeout(2000)

                if name == 'CLI_Contingencia':
                    select_single(page=self.page, value=value)
                else:
                    select_option(page=self.page, name=name, value=value)
                    self.frame.wait_for_timeout(2000)
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos gerais finalizado")
            return
        except Exception as e:
            message = e.args[0]
            self.classLogger.message(message)
            raise e
            