import json
import time
from urllib.parse import urlencode
from playwright.sync_api import Page, BrowserContext, sync_playwright
import requests

from modules.logger.Logger import Logger


class CadastrarEnvolvidoUseCase:
    def __init__(
        self,
        nome_envolvido:str,
        cpf_cnpj_envolvido: str,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.nome_envolvido = nome_envolvido
        self.cpf_cnpj_envolvido = cpf_cnpj_envolvido
        self.classLogger = classLogger
        self.context = context

    def execute(self)->dict:
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            tipo = "1" if len(self.cpf_cnpj_envolvido) == 14 else "2"
            cpf = self.cpf_cnpj_envolvido if tipo == "1" else ""
            cnpj = self.cpf_cnpj_envolvido if tipo == "2" else ""
            url = f"https://booking.nextlegalone.com.br/contatos/Contatos/EditModal"

            body = urlencode({
                "IsCpfCnpjObrigatorio":"False",
                "IsJustificativaObrigatoria":"False",
                "Nome":self.nome_envolvido,
                "Tipo":tipo,
                "CPF":cpf,
                "CNPJ":cnpj
            })

            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":url,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str,
                "Content-Type":"application/x-www-form-urlencoded"
            }

            response = requests.post(url=url,data=body,headers=headers)

            if response.status_code == 200:
                if 'O conte&#250;do informado no campo &#39;CPF&#39; n&#227;o &#233; v&#225;lido.' in response.text:
                    return CadastrarEnvolvidoUseCase(
                        nome_envolvido=self.nome_envolvido,
                        cpf_cnpj_envolvido='',
                        classLogger=self.classLogger,
                        context=self.context
                    ).execute()
                json_response = json.loads(response.text)
                return json_response
            raise Exception(response.text)
        except Exception as error:
            message = "Erro ao cadastrar o envolvido no Legalone"
            self.classLogger.message(message)
            raise error