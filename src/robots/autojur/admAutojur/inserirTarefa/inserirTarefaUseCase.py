from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.autojur.admAutojur.useCases.validarTarefaInserida.validarTarefaInseridaUseCase import ValidarTarefaInserida
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaTarefaFormatadosModel import (
    DadosEntradaTarefaFormatadosModel)
import time

class InserirTarefaUseCase:

    def __init__(self, page: Page, data_input: DadosEntradaTarefaFormatadosModel, localizador: str, classLogger: Logger) -> bool:
        self.page = page
        self.data_input = data_input
        self.localizador = localizador
        self.classLogger = classLogger

    def execute(self):
        message='Cadastrando os dados da tarefa na pasta do processo.'
        self.classLogger.message(message=message)
        self.page.query_selector("#btnAcoes\\:btnAddTarefa").click()
        time.sleep(5)
        iframe_url = self.page.query_selector("iframe").get_attribute('src')
        iframe = self.page.frame(url=f'https://baz.autojur.com.br{iframe_url}')
        time.sleep(1)
        iframe.query_selector("#formDetalhesTarefa\\:cmb-evento\\:ac-evento\\:ac-evento_input").type(self.data_input.evento)
        time.sleep(3)
        iframe.query_selector("#formDetalhesTarefa\\:responsavel\\:responsavel_input").click()
        time.sleep(1)
        iframe.query_selector("#formDetalhesTarefa\\:responsavel\\:responsavel_input").type(self.data_input.responsavel)
        time.sleep(2)
        iframe.query_selector("#formDetalhesTarefa\\:responsavel\\:responsavel_input").click()
        time.sleep(1)
        iframe.query_selector("#formDetalhesTarefa\\:data-final\\:datafinal_input").dblclick()
        time.sleep(2)
        iframe.query_selector("#formDetalhesTarefa\\:data-final\\:datafinal_input").type(f'{self.data_input.data} {self.data_input.hora}')
        time.sleep(3)
        iframe.query_selector("#formDetalhesTarefa\\:ff-conteudo\\:conteudo").click()
        time.sleep(1)
        iframe.query_selector("#formDetalhesTarefa\\:ff-conteudo\\:conteudo").type(f'{self.localizador}: {self.data_input.conteudo}')
        time.sleep(3)
        iframe.query_selector("#form-adicionar-tarefa\\:btn-salvar").click()
        time.sleep(5)

        error = ValidarTarefaInserida(page=self.page, data_input=self.data_input).execute()
        message='Tarefa cadastrada com êxito' if not error else 'Ocorreu um erro ao cadastrar a tarefa, entre em contato com o time de desenvolvimento'
        self.classLogger.message(message=message)
        
        return error