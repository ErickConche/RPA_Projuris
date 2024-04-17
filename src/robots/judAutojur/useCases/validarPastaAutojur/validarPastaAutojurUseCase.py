import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.judAutojur.useCases.validarPastaAutojur.__model__.CodigoModel import CodigoModel

class ValidarPastaAutojurUseCase:
    def __init__(
        self,
        page: Page,
        pasta:str, 
        processo: str,
        classLogger: Logger,
        retry: int = 0
    ) -> None:
        self.page = page
        self.pasta = pasta
        self.processo = processo
        self.classLogger = classLogger
        self.retry = retry

    def execute(self)->CodigoModel:
        try:
            attemp = 0
            max_attemp = 3
            while attemp < max_attemp:
                try:
                    self.page.goto("https://baz.autojur.com.br/sistema/processos/processo.jsf")
                    time.sleep(10)
                    self.page.locator('button[data-id="form-pesquisa:componente-pesquisa:cmb-campo-pesquisa-rapida"]').click()
                    time.sleep(1)
                    self.page.locator('#form-pesquisa\\:componente-pesquisa\\:campo .bs-searchbox input').click()
                    time.sleep(3)
                    self.page.locator('#form-pesquisa\\:componente-pesquisa\\:campo .bs-searchbox input').type("Localizador")
                    time.sleep(3)
                    self.page.locator('#form-pesquisa\\:componente-pesquisa\\:campo .dropdown-menu a:has(span:text-is("Localizador"))').click()
                    time.sleep(3)
                    self.page.locator('button[data-id="form-pesquisa:tipo-proc"]').click()
                    time.sleep(5)
                    self.page.locator('#form-pesquisa\\:pg-pesquisa-body .dropdown-menu a:has(span:text-is("Judicial"))').click()
                    time.sleep(5)
                    pastas = [self.pasta, self.pasta.replace("Pasta nº ",""), self.pasta.replace("Pasta n° ","")]
                    for pasta in pastas:
                        self.page.locator('#form-pesquisa\\:componente-pesquisa\\:txt-conteudo').click()
                        time.sleep(1)
                        self.page.locator('#form-pesquisa\\:componente-pesquisa\\:txt-conteudo').clear()
                        time.sleep(1)
                        self.page.locator('#form-pesquisa\\:componente-pesquisa\\:txt-conteudo').type(pasta)
                        time.sleep(1)
                        self.page.locator('#form-pesquisa\\:componente-pesquisa\\:btn-pesquisar').click()
                        time.sleep(10)
                        site_html = BeautifulSoup(self.page.content(), 'html.parser')
                        trs = site_html.select_one("#list-processos\\:tabela_data").select("tr")
                        if trs[0].text != 'Nenhum registro encontrado':
                            for tr in trs:
                                pasta_encontrada = tr.select('.lg-dado.tooltipstered')[3].next
                                processo = tr.select('.lg-dado.tooltipstered')[4].next
                                codigo_encontrado = tr.select('.lg-dado.tooltipstered')[0].next
                                if pasta_encontrada == pasta and processo == self.processo:
                                    message = f"A pasta informada possui um codigo já existente. Codigo: {codigo_encontrado}"
                                    self.classLogger.message(message)
                                    data_codigo: CodigoModel = CodigoModel(
                                        found=True,
                                        codigo=codigo_encontrado
                                    )
                                    return data_codigo
                                elif pasta_encontrada == self.pasta:
                                    message = f"Essa pasta já existe, porem o processo desse cadastro é o {processo}. Codigo: {codigo_encontrado}"
                                    self.classLogger.message(message)
                                    raise Exception (message)

                    message = "A pasta informada não possui um codigo existente"
                    self.classLogger.message(message)
                    data_codigo: CodigoModel = CodigoModel(
                        found=False,
                        codigo=None
                    )
                    return data_codigo
                except Exception as error:
                    attemp +=1
                    time.sleep(5)
        except Exception as error:
            raise Exception("Erro ao validar se a pasta já existe")
        
