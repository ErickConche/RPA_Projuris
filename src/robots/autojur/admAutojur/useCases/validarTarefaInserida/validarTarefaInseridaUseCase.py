from bs4 import BeautifulSoup
from playwright.sync_api import Page
import time
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaTarefaFormatadosModel import (
    DadosEntradaTarefaFormatadosModel)

class ValidarTarefaInserida:
    def __init__(self, page: Page, data_input: DadosEntradaTarefaFormatadosModel) -> bool:
        self.page = page
        self.data_input = data_input

    def execute(self):
        self.page.query_selector('[href="#tabview-pasta:tab-tarefa"]').click()
        time.sleep(5)
        site_html = BeautifulSoup(self.page.content(), 'html.parser')
        find_responsavel = site_html.find('span', string=self.data_input.responsavel)
        find_evento = site_html.find('span', string=self.data_input.evento)

        return False if find_evento and find_responsavel else True