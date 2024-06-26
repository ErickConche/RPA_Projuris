from playwright.sync_api import Frame, Page
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from modules.logger.Logger import Logger
from unidecode import unidecode

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
            frame = None
            iframe = self.page.query_selector_all('iframe')[-1]
            frame_name = iframe.get_attribute('name')
            frame_id = iframe.get_attribute('id')
            
            if frame_name or frame_id:
                frame = self.page.frame(name=frame_name) if frame_name else self.page.frame(id=frame_id)
            
            element = frame.wait_for_selector('[name="Tipo"]')
            if not element:
                raise Exception("Erro ao preencher partes")
            element.click()
            if cpfcnpj:
                selector = 'li[title="Pessoa Física"]' if len(cpfcnpj) <= 11 else 'li[title="Pessoa Jurídica"]'
                
                self.page.query_selector(selector).click()

                frame.evaluate('''() => {
                    const div = document.querySelector("#CPFCNPJ")
                    if (div) {
                        div.classList.remove('x-hide-display');
                    }
                }''')
                frame.fill("[name=CPFCNPJ]", cpfcnpj)
            frame.wait_for_selector('[name="NomeRazaoSocial"]').fill(value)
            button = frame.wait_for_selector('#bm-Save')
            # Deixar a ação click comentada para desenvolvimento ou se criar parte para teste confirmar a exclusão!!!
            button.click()
            frame.wait_for_timeout(2000)
            self.classLogger.message(f'Sucesso ao criar parte: {value}')
        except Exception as e:
            self.classLogger.message(e.args[0])
            raise e
        finally:
            frame.wait_for_selector('#Close').click()