import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.autojur.admAutojur.useCases.buscarDataCadastro.buscarDataCadastroUseCase import BuscarDataCadastroUseCase
from robots.autojur.__model__.CodigoModel import CodigoModel


class ValidarPastaAutojurTarefaUseCase:
    def __init__(
        self,
        page: Page,
        pasta:str,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.pasta = pasta
        self.classLogger = classLogger

    def execute(self)->CodigoModel:
        try:
            self.page.goto("https://baz.autojur.com.br/sistema/processos/processo.jsf")
            time.sleep(5)
            self.page.locator('button[data-id="form-pesquisa:componente-pesquisa:cmb-campo-pesquisa-rapida"]').click()
            time.sleep(3)
            self.page.locator('#form-pesquisa\\:componente-pesquisa\\:campo .bs-searchbox input').click()
            time.sleep(1)
            self.page.locator('#form-pesquisa\\:componente-pesquisa\\:campo .bs-searchbox input').type("Localizador")
            time.sleep(2)
            self.page.locator('#form-pesquisa\\:componente-pesquisa\\:campo .dropdown-menu a:has(span:text-is("Localizador"))').click()
            time.sleep(1)
            self.page.locator('#form-pesquisa\\:componente-pesquisa\\:txt-conteudo').click()
            time.sleep(1)
            self.page.locator('#form-pesquisa\\:componente-pesquisa\\:txt-conteudo').type(self.pasta)
            time.sleep(2)
            self.page.locator('button[data-id="form-pesquisa:tipo-proc"]').click()
            time.sleep(3)
            self.page.locator('#form-pesquisa\\:pg-pesquisa-body .dropdown-menu a:has(span:text-is("Extrajudicial"))').click()
            time.sleep(3)
            self.page.locator('#form-pesquisa\\:componente-pesquisa\\:btn-pesquisar').click()
            time.sleep(5)
            tr = self.page.query_selector("#list-processos\\:tabela_data > tr")
            if tr.inner_text() != 'Nenhum registro encontrado':
                protocol = tr.query_selector('.lg-dado.tooltipstered').inner_text()
                data_codigo = {
                    'codigo': protocol
                }
                tr.dblclick()
                time.sleep(5)
                return data_codigo
            else:
                raise Exception("Pasta não localizada")
            
        except Exception as error:
            raise Exception("Erro ao validar se a pasta já existe")
        
