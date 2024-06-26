from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
from unidecode import unidecode
from robots.espaider.useCases.helpers.selectOptionHelper import select_option, select_single
from robots.espaider.useCases.helpers.insertValueHelper import insert_value

class InserirDadosDesdobramentoUseCase:
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
            "ABA_DESD_OrgaoIDEdt",
            "ABA_DESD_dtaDataDistribuicaoEdt",
            "ABA_DESD_JuizoIDEdt",
            "ABA_DESD_BuscaComarcaIDEdt",
            "ABA_DESD_luInstanciaIDEdt",
            "ABA_DESD_txtNumeroEdt",
            "ABA_DESD_MeioTramitacaoEdt"
        ]
        
        try:
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos desdobramento principal iniciado")
            for name in name_inputs:
                self.input_value(name=name)
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos desdobramento principal finalizado")
            return
        except Exception as e:
            message = e.args[0]
            self.classLogger.message(message)
            raise e

    def input_value(self, name):
        de_para = {
            "ABA_DESD_OrgaoIDEdt":"orgao",
            "ABA_DESD_dtaDataDistribuicaoEdt":"data_distribuicao",
            "ABA_DESD_JuizoIDEdt":"juizo",
            "ABA_DESD_BuscaComarcaIDEdt":"comarca",
            "ABA_DESD_luInstanciaIDEdt":"instancia",
            "ABA_DESD_txtNumeroEdt":"processo",
            "ABA_DESD_MeioTramitacaoEdt":"peticionamento"
        }

        
        value = insert_value(data_input=self.data_input, de_para=de_para, name=name, frame=self.frame, tag="id")
        if name in ['ABA_DESD_dtaDataDistribuicaoEdt', 'ABA_DESD_txtNumeroEdt']:
            return
        select = self.frame.wait_for_selector(f'#{name}')
        if not select:
            raise(f'Erro ao preencher dados, campo: {name}')
        select.click()
        self.page.wait_for_timeout(2000)

        if name == 'ABA_DESD_MeioTramitacaoEdt':
            select_single(page=self.page, value=value)
        else:
            select_option(page=self.page, name=name, value=value)