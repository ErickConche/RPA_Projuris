import requests
from datetime import datetime
from bs4 import BeautifulSoup
from unidecode import unidecode
from urllib.parse import urlencode
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.autojur.identExpJudAutojur.useCases.validarEFormatarEntrada.__model__.codigoModel import CodigoModel
from robots.autojur.identExpJudAutojur.useCases.verificarProximoDiaUtil.verificarProximoDiaUtilUseCase import VerificarProximoDiaUtilUseCase
from robots.autojur.identExpJudAutojur.useCases.formatarData.formatarDatauseCase import formatarData

class ProcurarProcessoAutojurUseCase:
    def __init__(
        self,
        page: Page,
        processo: str,
        data_expediente: str,
        tipo_expediente: str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.page = page
        self.processo = processo.replace("-","").replace(".","")
        self.data_expediente = data_expediente
        self.tipo_expediente = tipo_expediente
        self.classLogger = classLogger
        self.context = context

    def execute(self)->CodigoModel:
        try:
            data_atual=datetime.now()
            dia=int(data_atual.strftime("%d"))
            mes=int(data_atual.strftime("%m"))
            ano=int(data_atual.strftime("%Y"))
            processo_encontrado = False
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
                "form-pesquisa:componente-pesquisa:txt-conteudo": self.processo,
                "form-pesquisa:tipo-proc": "4",
                "form-pesquisa:cmb-ordenacao": "-",
                "form-pesquisa:radio-status": "ATIVO"
            })

            response = requests.post(url=url, data=body, headers=headers)
            site_html = BeautifulSoup(BeautifulSoup(response.text, 'html.parser').select("update")[4].next, 'html.parser')
            try:
                trs = site_html.select_one("#list-processos\:tabela_data").select("tr")
                if trs[0].text != 'Nenhum registro encontrado':
                    processo_encontrado = True
                
                data_expediente = formatarData(self.data_expediente) if "audiencia" in self.tipo_expediente.lower().replace('ê', 'e') else VerificarProximoDiaUtilUseCase(ano, mes, dia).exec()
                data_codigo: CodigoModel = CodigoModel(
                    processo=self.processo,
                    data_expediente=data_expediente,
                    processo_cadastrado='Sim' if processo_encontrado else 'Nao'
                )

                return data_codigo
            except Exception as error:
                raise Exception("Erro ao filtrar os processos através do campo do número do CNJ/Processo informado")
            
        except Exception as e:
            raise ValueError("Erro ao tentar fazer a busca no sistema do Autojur!")
