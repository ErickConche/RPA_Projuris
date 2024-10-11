from playwright.sync_api import Page, Frame
from modules.logger.Logger import Logger
import time

class CriarOrgaoUseCase:
    def __init__(self, page: Page, classLogger: Logger, name: str) -> None:
        self.page = page
        self.classLogger = classLogger
        self.value = name

    def execute(self):
        self.classLogger.message('Iniciando cadastro do Órgão')
        inserted = False
        self.page.query_selector('[class="x-popup x-anim-fade x-popup-grid-menu x-elevation-z8 x-layout--container"] > div > div > div > div > button[data-icon="add_circle"]').click()
        time.sleep(2)
        frame = self.get_frame()
        frame.query_selector("[name=Nome]").type(self.value)
        self.save_orgao(frame=frame)
        self.close_frame(frame=frame)
        
    def get_frame(self) -> Frame:
        """Obtém o último iframe disponível e retorna o frame correspondente."""
        iframe = self.page.query_selector_all('iframe')[-1]
        frame_name = iframe.get_attribute('name')
        frame_id = iframe.get_attribute('id')
        
        if frame_name:
            return self.page.frame(name=frame_name)
        elif frame_id:
            return self.page.frame(id=frame_id)
        else:
            raise Exception("Frame não encontrado.")

    def save_orgao(self, frame: Frame) -> None:
        """Salva a parte no sistema."""
        button = frame.wait_for_selector('#bm-Save')
        # Mantenha o click comentado para evitar criar partes no teste
        button.click()
        frame.wait_for_timeout(10000)
        self.classLogger.message(f'Sucesso ao criar órgão: {self.value}')

    def close_frame(self, frame: Frame) -> None:
        """Fecha o frame após a execução."""
        frame.wait_for_selector('#Close').click()
        time.sleep(5)