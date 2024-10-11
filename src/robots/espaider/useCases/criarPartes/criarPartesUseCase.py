from playwright.sync_api import Frame, Page
import re
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
from unidecode import unidecode
from robots.espaider.useCases.helpers.selectOptionHelper import select_option

class CriarPartesUseCase:
    def __init__(
        self, 
        page: Page,
        frame: Frame,
        data_input: DadosEntradaEspaiderModel,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self, value, cpfcnpj=''):
        try:
            frame = self.get_frame()
            self.select_tipo(frame)
            
            if cpfcnpj:
                self.process_cpf_cnpj(frame, cpfcnpj)
            else:
                raise Exception('Erro ao criar parte, Cpf/Cnpj incorreto')
            
            self.fill_nome_razao_social(frame, value)
            self.save_part(frame, value)

        except Exception as e:
            self.classLogger.message(e.args[0])
            raise e
        finally:
            self.close_frame(frame)

    def get_frame(self) -> Frame:
        iframe = self.page.query_selector_all('iframe')[-1]
        frame_name = iframe.get_attribute('name')
        frame_id = iframe.get_attribute('id')
        
        if frame_name:
            return self.page.frame(name=frame_name)
        elif frame_id:
            return self.page.frame(id=frame_id)
        else:
            raise Exception("Frame não encontrado.")

    def select_tipo(self, frame: Frame) -> None:
        element = frame.wait_for_selector('[name="Tipo"]')
        if not element:
            raise Exception("Erro ao preencher partes")
        element.click()

    def process_cpf_cnpj(self, frame: Frame, cpfcnpj: str) -> None:
        cpfcnpj_cleaned = re.sub(r'[^\w\s]', '', cpfcnpj)
        is_cpf = len(cpfcnpj_cleaned) <= 11
        is_oab = "oab" in cpfcnpj_cleaned.lower()
        selector = 'li[title="Pessoa Física"]' if is_cpf else 'li[title="Pessoa Jurídica"]'
        
        self.page.query_selector(selector).click()
        if is_oab:
            pass
        elif is_cpf:
            frame.fill("[name=CPF]", cpfcnpj)
        elif not is_cpf:
            self.reveal_cpf_cnpj_field(frame)
            frame.fill("[name=CPFCNPJ]", cpfcnpj)
            self.fill_tipo_estabelecimento(frame)

    def reveal_cpf_cnpj_field(self, frame: Frame) -> None:
        frame.evaluate('''() => {
            const div = document.querySelector("#CPFCNPJ")
            if (div) {
                div.classList.remove('x-hide-display');
            }
        }''')

    def fill_tipo_estabelecimento(self, frame: Frame) -> None:
        frame.query_selector('[name="CLI_TipoEstabelecimento"]').type('Matriz')
        select_option(page=self.page, name="CLI_TipoEstabelecimento", value="Matriz")

    def fill_nome_razao_social(self, frame: Frame, value: str) -> None:
        frame.wait_for_selector('[name="NomeRazaoSocial"]').fill(value)

    def save_part(self, frame: Frame, value: str) -> None:
        button = frame.wait_for_selector('#bm-Save')
        button.click()
        frame.wait_for_timeout(10000)
        self.classLogger.message(f'Sucesso ao criar parte: {value}')

    def close_frame(self, frame: Frame) -> None:
        frame.wait_for_selector('#Close').click()
