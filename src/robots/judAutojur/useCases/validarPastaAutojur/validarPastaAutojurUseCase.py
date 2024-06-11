import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.judAutojur.useCases.validarPastaAutojur.__model__.CodigoModel import CodigoModel
from robots.judAutojur.useCases.buscarDataCadastro.buscarDataCadastroUseCase import BuscarDataCadastroUseCase


class ValidarPastaAutojurUseCase:
    def __init__(
        self,
        page: Page,
        pasta:str, 
        processo: str,
        classLogger: Logger,
        context: BrowserContext,
        retry: int = 0
    ) -> None:
        self.page = page
        self.pasta = pasta
        self.processo = processo
        self.classLogger = classLogger
        self.retry = retry
        self.context = context

    def execute(self)->CodigoModel:
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'

            url = "https://baz.autojur.com.br/sistema/processos/processo.jsf"
            headers = {
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Cookie":cookies_str
            }
            response = requests.get(url=url, headers=headers)
            site_html = BeautifulSoup(response.text, 'html.parser')
            view_state = site_html.select_one("#form-pesquisa").find('input', {'name': 'javax.faces.ViewState'}).attrs.get('value')
            body = urlencode({
                "javax.faces.partial.ajax":"true",
                "javax.faces.source":"j_idt52",
                "primefaces.ignoreautoupdate":"true",
                "javax.faces.partial.execute":"j_idt52",
                "javax.faces.partial.render":"j_idt52",
                "j_idt52":"j_idt52",
                "j_idt52_load":"true",
                "menu-top":"menu-top",
                "javax.faces.ViewState": view_state
            })
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            response = requests.post(url=url,  data=body, headers=headers)

            body = urlencode({
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "form-pesquisa:componente-pesquisa:cmb-campo-pesquisa-rapida",
                "javax.faces.partial.execute": f"orm-pesquisa:componente-pesquisa:campo",
                "javax.faces.partial.render": "form-pesquisa:componente-pesquisa:operador form-pesquisa:componente-pesquisa:valor form-pesquisa:componente-pesquisa:campo",
                "javax.faces.behavior.event": "change",
                "javax.faces.partial.event": "change",
                "form-pesquisa": "form-pesquisa",
                "javax.faces.ViewState": view_state,
                "form-pesquisa:componente-pesquisa:cmb-campo-pesquisa-rapida": "43",
                "form-pesquisa:componente-pesquisa:j_idt301": "1",
                "form-pesquisa:componente-pesquisa:txt-conteudo": "",
                "form-pesquisa:tipo-proc": "4",
                "form-pesquisa:cmb-ordenacao": "-",
                "form-pesquisa:radio-status": "ATIVO"
            })

            response = requests.post(url=url,  data=body, headers=headers)

            pastas = [self.pasta, self.pasta.replace("Pasta nº ",""), self.pasta.replace("Pasta n° ","")]
            for pasta in pastas:
                body = urlencode({
                    "javax.faces.partial.ajax": "true",
                    "javax.faces.source": "form-pesquisa:componente-pesquisa:btn-pesquisar",
                    "javax.faces.partial.execute": "form-pesquisa:componente-pesquisa:pesquisa-rapida form-pesquisa list-processos:tabela",
                    "javax.faces.partial.render": "list-processos btnAcoes:btnAddTarefa btnAcoes:btn-editar btnAcoes:gerarFinanceiro form-pesquisa:componente-pesquisa:pesquisa-rapida",
                    "form-pesquisa:componente-pesquisa:btn-pesquisar": "form-pesquisa:componente-pesquisa:btn-pesquisar",
                    "form-pesquisa": "form-pesquisa",
                    "javax.faces.ViewState": view_state,
                    "form-pesquisa:componente-pesquisa:cmb-campo-pesquisa-rapida": "43",
                    "form-pesquisa:componente-pesquisa:j_idt301": "1",
                    "form-pesquisa:componente-pesquisa:txt-conteudo": pasta,
                    "form-pesquisa:tipo-proc": "4",
                    "form-pesquisa:cmb-ordenacao": "-",
                    "form-pesquisa:radio-status": "ATIVO"
                })

                response = requests.post(url=url,  data=body, headers=headers)

                site_html = BeautifulSoup(BeautifulSoup(response.text, 'html.parser').select("update")[4].next, 'html.parser')
                trs = site_html.select_one("#list-processos\\:tabela_data").select("tr")
                if trs[0].text != 'Nenhum registro encontrado':
                    pasta_duplicada = False
                    for tr in trs:
                        pasta_encontrada = tr.select('.lg-dado')[3].next
                        pasta_encontrada_split = pasta_encontrada.split("Cont")
                        pasta_encontrada_split = f"Cont{pasta_encontrada_split[1]}" if len(pasta_encontrada_split) > 1 else pasta_encontrada
                        pasta_split = pasta.split("Cont")
                        pasta_split = f"Cont{pasta_split[1]}" if len(pasta_split) > 1 else pasta
                        processo = tr.select('.lg-dado')[4].next
                        codigo_encontrado = tr.select('.lg-dado')[0].next
                        if pasta_encontrada_split == pasta_split and processo == self.processo:
                            message = f"A pasta informada possui um codigo já existente. Codigo: {codigo_encontrado}"
                            self.classLogger.message(message)
                            data_cadastro_encontrado = BuscarDataCadastroUseCase(
                                view_state=view_state,
                                headers=headers,
                                url=url,
                                classLogger=self.classLogger,
                                tr=tr
                            ).execute()
                            data_codigo: CodigoModel = CodigoModel(
                                found=True,
                                codigo=codigo_encontrado,
                                data_cadastro=data_cadastro_encontrado
                            )
                            return data_codigo
                        elif pasta_encontrada_split == pasta_split:
                            pasta_duplicada = True
                    if pasta_duplicada:
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
            raise Exception("Erro ao validar se a pasta já existe")
        
