import json
import requests
import urllib.parse
from unidecode import unidecode
from modules.logger.Logger import Logger
from playwright.sync_api import BrowserContext
from robots.legalone.useCases.cadastrarEnvolvido.cadastrarEnvolvidoUseCase import CadastrarEnvolvidoUseCase


class BuscarEnvolvidoUseCase:
    def __init__(
        self,
        nome_envolvido:str,
        cpf_cnpj_envolvido: str,
        classLogger: Logger,
        context: BrowserContext,
        retry: bool = False
    ) -> None:
        self.nome_envolvido = nome_envolvido
        self.cpf_cnpj_envolvido = cpf_cnpj_envolvido if cpf_cnpj_envolvido != '0' else ''
        self.classLogger = classLogger
        self.context = context
        self.retry = retry

    def execute(self)->dict:
        try:
            nomereclamante_format = urllib.parse.quote(self.nome_envolvido)
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = f"https://booking.nextlegalone.com.br/contatos/Contatos/LookupGridContato?positionId=1&term={nomereclamante_format}&pageSize=100&_=170"
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
                    classLogger=self.classLogger,
                    context=self.context
                ).execute()
            for row in json_response.get('Rows'):
                if unidecode(row.get("Value").upper()) == unidecode(self.nome_envolvido.upper()) \
                and (row.get("ContatoCPF_CNPJ") == self.cpf_cnpj_envolvido or self.cpf_cnpj_envolvido == ''):
                    return row
                
            return CadastrarEnvolvidoUseCase(
                nome_envolvido=self.nome_envolvido,
                cpf_cnpj_envolvido=self.cpf_cnpj_envolvido,
                classLogger=self.classLogger,
                context=self.context
            ).execute()
        except Exception as error:
            if not self.retry:
                return BuscarEnvolvidoUseCase(
                    nome_envolvido=self.nome_envolvido,
                    cpf_cnpj_envolvido='',
                    classLogger=self.classLogger,
                    context=self.context,
                    retry=True
                ).execute()
            message = "Erro ao buscar o cadastro do envolvido no Legalone"
            self.classLogger.message(message)
            raise error