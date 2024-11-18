import requests
from playwright.sync_api import Page, BrowserContext
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from modules.logger.Logger import Logger
from robots.autojur.identCadastroAutojur.useCases.validarEFormatarEntrada.__model__.codigoModel import CodigoModel

class ProcurarProcessoAdmAutojur:
    def __init__(
        self,
        page: Page,
        reclamacao: str,
        pessoa: str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.page = page
        self.reclamacao = reclamacao
        self.pessoa = pessoa
        self.classLogger = classLogger
        self.context = context

    def execute(self)->CodigoModel:
        try:
            if self.pessoa == '' or self.pessoa is None:
                data_codigo = [{
                    "Status":"Informe o nome da parte contrária!",
                    "Protocolo":""
                }]
                return data_codigo
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
                "javax.faces.source":"j_idt51",
                "primefaces.ignoreautoupdate":"true",
                "javax.faces.partial.execute":"j_idt51",
                "javax.faces.partial.render":"j_idt51",
                "j_idt52":"j_idt51",
                "j_idt52_load":"true",
                "menu-top":"menu-top",
                "javax.faces.ViewState": view_state
            })
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            response = requests.post(url=url,  data=body, headers=headers)

            body = urlencode({
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "form-pesquisa:componente-pesquisa:btn-pesquisar",
                "javax.faces.partial.execute": "form-pesquisa:componente-pesquisa:pesquisa-rapida form-pesquisa list-processos:tabela",
                "javax.faces.partial.render": "list-processos btnAcoes:btnAddTarefa btnAcoes:btn-editar btnAcoes:gerarFinanceiro form-pesquisa:componente-pesquisa:pesquisa-rapida",
                "form-pesquisa:componente-pesquisa:btn-pesquisar": "form-pesquisa:componente-pesquisa:btn-pesquisar",
                "form-pesquisa": "form-pesquisa",
                "javax.faces.ViewState": view_state,
                "form-pesquisa:componente-pesquisa:cmb-campo-pesquisa-rapida": "80",
                "form-pesquisa:componente-pesquisa:j_idt301": "1",
                "form-pesquisa:componente-pesquisa:txt-conteudo": self.reclamacao,
                "form-pesquisa:tipo-proc": "3",
                "form-pesquisa:cmb-ordenacao": "-",
                "form-pesquisa:radio-status": "ATIVO"
            })

            response = requests.post(url=url, data=body, headers=headers)
            site_html = BeautifulSoup(BeautifulSoup(response.text, 'html.parser').select("update")[4].next, 'html.parser')
            try:
                trs = site_html.select_one("#list-processos\:tabela_data").select("tr")
                if trs[0].text != 'Nenhum registro encontrado':
                    dados_processo = site_html.select_one("#list-processos\:tabela_data").select("span")
                    pasta = dados_processo[3].text
                    if self.pessoa.lower().strip() != dados_processo[21].text.lower().strip():
                        data_codigo: CodigoModel = CodigoModel(
                            status='Parte contrária informada não corresponde a parte cadastrada na pasta',
                            protocolo=pasta
                        )
                        raise Exception("Parte contrária informada não corresponde a parte cadastrada na pasta")
                    data_codigo: CodigoModel = CodigoModel(
                        status='Processo cadastrado',
                        protocolo=pasta
                    )
                else:
                    data_codigo: CodigoModel = CodigoModel(
                        status='Processo não encontrado',
                        protocolo=''
                    )
            except Exception as error:
                raise Exception("Erro ao filtrar os processos através dos dados fornecidos")
            finally:
                return data_codigo
            
        except Exception as e:
            raise ValueError("Erro ao tentar fazer a busca no sistema do Autojur!")