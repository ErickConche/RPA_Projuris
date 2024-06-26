from playwright.sync_api import Frame, Page
import re
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
from unidecode import unidecode
from robots.espaider.useCases.helpers.createPartHelper import criar_parte
from robots.espaider.useCases.helpers.selectOptionHelper import select_option, select_single

class InserirOutrasPartesUseCase:
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

    def execute(self, indice):
        name_inputs = [
            "Desdobramento",
            "Pessoa",
            "Classe",
            "Condicao"
        ]

        de_para = {
            "Desdobramento":"desdobramento",
            "Pessoa":f"parte_contraria_{indice}",
            "Classe":"classe_partes",
            "Condicao":f"condicao_parte_processo_{indice}"
        }
        
        try:
            for name in name_inputs:
                selected = False
                self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos partes do processo [outros] iniciado")
                value = getattr(self.data_input, de_para[name])
                if name == "Pessoa":
                    value = getattr(self.data_input, f"cpf_cnpj_parte_processo_{indice}")
                if name != "Pessoa":
                    value = "Ação de Repetição de Indébito" if name == "Desdobramento" else "Litisconsorte"
                value = unidecode(value).lower()
                if not value:
                    continue
                if name != "Classe":
                    input = self.frame.wait_for_selector(f'[name={name}]')
                    input.fill(value)
                self.frame.wait_for_selector(f"[name={name}]").click()
                self.frame.wait_for_timeout(2000)

                if name == "Classe":
                    select_single(page=self.page, value=value)
                else:
                    self.select_option(value=value, name=name, name_parte=getattr(self.data_input, f"parte_contraria_{indice}"))
                    continue

                if not selected:
                    raise(f'Erro ao preencher dados, campo: {name}')

            ###
            self.frame.wait_for_selector("#bm-Save").click()
            self.frame.wait_for_timeout(2000)
            
            self.frame.wait_for_selector("#Close")
            self.classLogger.message("[Espaider-Civil]: Preenchimento dos campos partes do processo [outros] finalizado")
            return
        except Exception as e:
            message = e.args[0]
            self.classLogger.message(message)
            raise e

    def select_option(self, value, name, name_parte):
        selected = select_option(page=self.page, name=name, value=value)
        if not selected:
            criar_parte(
                value=self.data_input.parte_contraria, 
                cpfcnpj=self.data_input.cpf_cnpj_parte_contraria, 
                page=self.page, 
                frame=self.frame, 
                data_input=self.data_input, 
                classLogger=self.classLogger
            )
            return self.select_option(value=value, name=name, name_parte=name_parte)
        return selected