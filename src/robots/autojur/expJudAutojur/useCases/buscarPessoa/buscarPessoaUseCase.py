import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from urllib.parse import urlencode
from modules.logger.Logger import Logger


class BuscarPessoaUseCase:
    def __init__(
        self,
        classLogger: Logger,
        cookies: str,
        nome: str
    ) -> None:
        self.classLogger = classLogger
        self.cookies = cookies
        self.nome = nome

    def execute(self) -> str:
        url = "https://baz.autojur.com.br/sistema/pessoa/pessoa.jsf"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": self.cookies
        }
        response = requests.get(url=url, headers=headers)
        site_html = BeautifulSoup(response.text, 'html.parser')
        view_state = site_html.select_one(".form-pesquisa").find('input', {'name': 'javax.faces.ViewState'}).attrs.get('value')

        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "cadastro:ativo:0",
            "javax.faces.partial.execute": "cadastro:ativo",
            "javax.faces.partial.render": "cadastro:tabela cadastro:btnEdit cadastro:btnExcluir cadastro:pg-timesheet",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
            "cadastro": "cadastro",
            "javax.faces.ViewState": view_state,
            "cadastro:componente-pesquisa:cmb-campo-pesquisa-rapida": "30",
            "cadastro:componente-pesquisa:j_idt296": "1",
            "cadastro:componente-pesquisa:txt-conteudo": "",
            "cadastro:cmbCategoriaPessoa": "-",
            "cadastro:ativo": "0",
            "cadastro:tabela_rppDD": "20",
            "cadastro:tabela_selection": ""
        })

        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        response = requests.post(url=url,  data=body, headers=headers)

        pesquisa_campo_rapido = "30"
        valor_busca = self.nome

        body = urlencode({
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "cadastro:componente-pesquisa:btn-pesquisar",
            "javax.faces.partial.execute": "cadastro:componente-pesquisa:pesquisa-rapida",
            "javax.faces.partial.render": "cadastro:tabela cadastro:btnEdit cadastro:btnExcluir cadastro:pg-timesheet cadastro:componente-pesquisa:pesquisa-rapida",
            "cadastro:componente-pesquisa:btn-pesquisar": "cadastro:componente-pesquisa:btn-pesquisar",
            "cadastro": "cadastro",
            "javax.faces.ViewState": view_state,
            "cadastro:componente-pesquisa:cmb-campo-pesquisa-rapida": pesquisa_campo_rapido,
            "cadastro:componente-pesquisa:j_idt296": "1",
            "cadastro:componente-pesquisa:txt-conteudo": valor_busca,
            "cadastro:cmbCategoriaPessoa": "-",
            "cadastro:ativo": "0",
            "cadastro:tabela_rppDD": "20",
            "cadastro:tabela_selection": "",
        })
        response = requests.post(url=url, data=body, headers=headers)

        site_html = BeautifulSoup(BeautifulSoup(response.text, 'html.parser').select("update")[4].next, 'html.parser')
        trs = site_html.select_one("#cadastro\\:tabela_data").select("tr")
        if trs[0].text == 'Nenhum registro encontrado':
            message = "Responsável não encontrado"
            self.classLogger.message(message)
        else:
            for tr in trs:
                tds = tr.select("td")
                if unidecode(tds[3].previous.upper()) == unidecode(self.nome.upper()):
                    return tds[0].text
