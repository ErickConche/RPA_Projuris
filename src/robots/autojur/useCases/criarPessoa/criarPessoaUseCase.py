import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from modules.logger.Logger import Logger
from robots.autojur.useCases.listarEnvolvidos.__model__.ObjEnvolvidosModel import ObjEnvolvidosModel


class CriarPessoaUseCase:
    def __init__(
        self,
        classLogger: Logger,
        headers: dict,
        envolvido: ObjEnvolvidosModel,
        view_state: str,
        pesquisa_campo_rapido: str
    ) -> None:
        self.classLogger = classLogger
        self.envolvido = envolvido
        self.headers = headers
        self.view_state = view_state
        self.pesquisa_campo_rapido = pesquisa_campo_rapido

    def execute(self)->ObjEnvolvidosModel:
        try:
            url = "https://baz.autojur.com.br/sistema/pessoa/pessoa.jsf"
            body = urlencode({
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "cadastro:j_idt356",
                "javax.faces.partial.execute": "@all",
                "cadastro:j_idt356": "cadastro:j_idt356",
                "cadastro": "cadastro",
                "javax.faces.ViewState": self.view_state,
                "cadastro:componente-pesquisa:cmb-campo-pesquisa-rapida": self.pesquisa_campo_rapido,
                "cadastro:componente-pesquisa:j_idt295": "1",
                "cadastro:componente-pesquisa:txt-conteudo": "",
                "cadastro:cmbCategoriaPessoa": "-",
                "cadastro:ativo": "0",
                "cadastro:tabela_rppDD": "20",
                "cadastro:tabela_selection": "",
            })

            response = requests.post(url=url, data=body, headers=self.headers)

            text = BeautifulSoup(response.text, 'html.parser').select_one("eval").next
            regex = r"pfdlgcid:'(.*?)'"
            id = re.search(regex, text).group(1).replace("\\","")

            url = f"https://baz.autojur.com.br/sistema/mdPessoa.jsf?uuidPessoa=&retornarCadastro=false&pfdlgcid={id}"

            response = requests.get(url=url, headers=self.headers)

            site_html = BeautifulSoup(response.text, 'html.parser')

            view_state = site_html.select_one("#form-tipo-pessoa").find('input', {'name': 'javax.faces.ViewState'}).attrs.get('value')
            tipo_pessoa = "JURIDICA" if len(self.envolvido.cpf_cnpj) > 14 else "FISICA"
            if len(self.envolvido.cpf_cnpj) > 14:
                body = urlencode({
                    "javax.faces.partial.ajax": "true",
                    "javax.faces.source": "form-tipo-pessoa:j_idt26:tipo:1",
                    "javax.faces.partial.execute": "form-tipo-pessoa",
                    "javax.faces.partial.render": "tabs form-tipo-pessoa:ff-cpf-cnpj",
                    "javax.faces.behavior.event": "valueChange",
                    "javax.faces.partial.event": "change",
                    "form-tipo-pessoa": "form-tipo-pessoa",
                    "javax.faces.ViewState": view_state,
                    "form-tipo-pessoa:j_idt26:tipo": tipo_pessoa,
                    "form-tipo-pessoa:ff-nome:nome": "",
                    "form-tipo-pessoa:ff-cpf-cnpj:j_idt29": ""
                })
                response = requests.post(url=url,  data=body, headers=self.headers)

            body = urlencode({
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "form-tipo-pessoa:ff-nome:nome",
                "javax.faces.partial.execute": "form-tipo-pessoa:ff-nome:nome",
                "javax.faces.behavior.event": "change",
                "javax.faces.partial.event": "change",
                "form-tipo-pessoa": "form-tipo-pessoa",
                "javax.faces.ViewState": view_state,
                "form-tipo-pessoa:j_idt26:tipo": tipo_pessoa,
                "form-tipo-pessoa:ff-nome:nome": self.envolvido.nome,
                "form-tipo-pessoa:ff-cpf-cnpj:j_idt29": ""
            })

            response = requests.post(url=url,  data=body, headers=self.headers)

            body = urlencode({
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "form-tipo-pessoa:ff-cpf-cnpj:j_idt29",
                "javax.faces.partial.execute": "form-tipo-pessoa:ff-cpf-cnpj:j_idt29",
                "javax.faces.behavior.event": "change",
                "javax.faces.partial.event": "change",
                "form-tipo-pessoa": "form-tipo-pessoa",
                "javax.faces.ViewState": view_state,
                "form-tipo-pessoa:j_idt26:tipo": tipo_pessoa,
                "form-tipo-pessoa:ff-nome:nome": self.envolvido.nome,
                "form-tipo-pessoa:ff-cpf-cnpj:j_idt29": self.envolvido.cpf_cnpj
            })

            response = requests.post(url=url,  data=body, headers=self.headers)

            body = urlencode({
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "form-salvar-pessoa:j_idt658",
                "javax.faces.partial.execute": "form-tipo-pessoa form-salvar-pessoa:j_idt658",
                "form-salvar-pessoa:j_idt658": "form-salvar-pessoa:j_idt658",
                "form-tipo-pessoa": "form-tipo-pessoa",
                "javax.faces.ViewState": view_state,
                "form-tipo-pessoa:j_idt26:tipo": tipo_pessoa,
                "form-tipo-pessoa:ff-nome:nome": self.envolvido.nome,
                "form-tipo-pessoa:ff-cpf-cnpj:j_idt29": self.envolvido.cpf_cnpj
            })

            response = requests.post(url=url,  data=body, headers=self.headers)

            duplicate = BeautifulSoup(response.text, 'html.parser').select("eval")
            if duplicate and duplicate[0].next == "showModal('#modal-duplicados')":
                self.envolvido.cpf_cnpj = ''
                return CriarPessoaUseCase(
                    classLogger=self.classLogger,
                    headers=self.headers,
                    envolvido=self.envolvido,
                    view_state=self.view_state,
                    pesquisa_campo_rapido=self.pesquisa_campo_rapido
                ).execute()
            return self.envolvido
        except Exception as error:
            message = f"Erro ao inserir pessoa {self.envolvido.nome}"
            self.classLogger.message(message)
            raise Exception ("Erro ao inserir dos outros envolvidos")