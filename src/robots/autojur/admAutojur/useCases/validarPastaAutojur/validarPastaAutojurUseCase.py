import time
from bs4 import BeautifulSoup
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.autojur.__model__.CodigoModel import CodigoModel


class ValidarPastaAutojurUseCase:
    def __init__(
        self,
        page: Page,
        pasta:str, 
        numero_reclamacao: str,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.pasta = pasta
        self.numero_reclamacao = numero_reclamacao
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
            time.sleep(1)
            self.page.locator('#form-pesquisa\\:componente-pesquisa\\:campo .dropdown-menu a:has(span:text-is("Localizador"))').click()
            time.sleep(1)
            self.page.locator('#form-pesquisa\\:componente-pesquisa\\:txt-conteudo').click()
            time.sleep(1)
            self.page.locator('#form-pesquisa\\:componente-pesquisa\\:txt-conteudo').type(self.pasta)
            time.sleep(1)
            self.page.locator('button[data-id="form-pesquisa:tipo-proc"]').click()
            time.sleep(3)
            self.page.locator('#form-pesquisa\\:pg-pesquisa-body .dropdown-menu a:has(span:text-is("Extrajudicial"))').click()
            time.sleep(3)
            self.page.locator('#form-pesquisa\\:componente-pesquisa\\:btn-pesquisar').click()
            time.sleep(5)
            site_html = BeautifulSoup(self.page.content(), 'html.parser')
            trs = site_html.select_one("#list-processos\\:tabela_data").select("tr")
            if trs[0].text != 'Nenhum registro encontrado':
                for tr in trs:
                    pasta_encontrada = tr.select('.lg-dado.tooltipstered')[3].next
                    numero_reclamacao_encontrada = tr.select('.lg-dado.tooltipstered')[4].next
                    codigo_encontrado = tr.select('.lg-dado.tooltipstered')[0].next
                    if pasta_encontrada == self.pasta and numero_reclamacao_encontrada == self.numero_reclamacao:
                        message = f"A pasta informada possui um codigo já existente. Codigo: {codigo_encontrado}"
                        self.classLogger.message(message)
                        data_codigo: CodigoModel = CodigoModel(
                            found=True,
                            codigo=codigo_encontrado
                        )
                        return data_codigo
            
            message = "A pasta informada não possui um codigo existente"
            self.classLogger.message(message)
            data_codigo: CodigoModel = CodigoModel(
                found=False,
                codigo=None
            )
            return data_codigo
            
        except Exception as error:
            raise Exception("Erro ao validar se a pasta já existe")
        