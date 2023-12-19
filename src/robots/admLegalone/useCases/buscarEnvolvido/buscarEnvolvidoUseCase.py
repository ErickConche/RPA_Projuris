import json
from playwright.sync_api import Page, BrowserContext, sync_playwright
import requests

from modules.logger.Logger import Logger
from robots.admLegalone.useCases.cadastrarEnvolvido.cadastrarEnvolvidoUseCase import CadastrarEnvolvidoUseCase

class BuscarEnvolvidoUseCase:
    def __init__(
        self,
        nome_envolvido:str,
        cpf_cnpj_envolvido: str,
        tipo_envolvido:str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.nome_envolvido = nome_envolvido
        self.cpf_cnpj_envolvido = cpf_cnpj_envolvido
        self.tipo_envolvido = tipo_envolvido
        self.classLogger = classLogger
        self.context = context

    def execute(self)->dict:
        try:
            nomereclamante_format = self.nome_envolvido.replace(" ","+")
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = f"https://booking.nextlegalone.com.br/contatos/Contatos/LookupGridContato?term={nomereclamante_format}&pageSize=10&_=1702910899371"
            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":url,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }
            response = requests.get(url=url,headers=headers)

            json_response = json.loads(response.text)
            if json_response.get('Count')<=0:
                return CadastrarEnvolvidoUseCase(
                    nome_envolvido=self.nome_envolvido,
                    cpf_cnpj_envolvido=self.cpf_cnpj_envolvido,
                    tipo_envolvido=self.tipo_envolvido,
                    classLogger=self.classLogger,
                    context=self.context
                ).execute()
            for row in json_response.get('Rows'):
                if row.get("Value") == self.nome_envolvido and row.get("ContatoCPF_CNPJ") == self.cpf_cnpj_envolvido:
                    return row
                
            return CadastrarEnvolvidoUseCase(
                nome_envolvido=self.nome_envolvido,
                cpf_cnpj_envolvido=self.cpf_cnpj_envolvido,
                tipo_envolvido=self.tipo_envolvido,
                classLogger=self.classLogger,
                context=self.context
            ).execute()
        except Exception as error:
            message = "Erro ao buscar o cadastro do envolvido no Legalone"
            self.classLogger.message(message)
            raise error