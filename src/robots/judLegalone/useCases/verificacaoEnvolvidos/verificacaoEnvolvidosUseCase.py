import json
import time
from urllib.parse import quote
from playwright.sync_api import Page, BrowserContext, sync_playwright
import requests
from unidecode import unidecode

from modules.logger.Logger import Logger
from robots.judLegalone.useCases.alterarObjetoEntrada.alterarObjetoEntradaUseCase import AlterarObjetoEntradaUseCase
from robots.judLegalone.useCases.listarEnvolvidos.listarEnvolvidosUseCase import ListarEnvolvidosUseCase
from robots.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class VerificacaoEnvolvidosUseCase:
    def __init__(
        self,
        classLogger: Logger,
        data_input: DadosEntradaFormatadosModel,
        context: BrowserContext
    ) -> None:
        self.classLogger = classLogger
        self.context = context
        self.data_input = data_input

    def execute(self)->DadosEntradaFormatadosModel:
        try:
            lista_envolvidos = ListarEnvolvidosUseCase(
                classLogger=self.classLogger,
                data_input=self.data_input
            ).execute()
            for obj_envolvido in lista_envolvidos:
                if obj_envolvido.cpf_cnpj != '':
                    cookies = self.context.cookies()
                    cookies_str = ''
                    for cookie in cookies:
                        cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
                    url = f"https://booking.nextlegalone.com.br/contatos/Contatos/LookupGridContato?positionId=1&term={quote(obj_envolvido.cpf_cnpj)}&pageSize=10&_=170"
                    headers = {
                        "X-Requested-With":"XMLHttpRequest",
                        "Referer":url,
                        "Host":"booking.nextlegalone.com.br",
                        "Cookie":cookies_str
                    }
                    response = requests.get(url=url,headers=headers)

                    json_response = json.loads(response.text)

                    for row in json_response.get('Rows'):
                        if row.get("ContatoCPF_CNPJ") == obj_envolvido.cpf_cnpj:
                            if unidecode(row.get("Value").upper()) != unidecode(obj_envolvido.nome.upper()):
                                self.data_input = AlterarObjetoEntradaUseCase(
                                    data_input=self.data_input,
                                    valor=row.get("Value"),
                                    chave=obj_envolvido.tag_objeto,
                                    classLogger=self.classLogger
                                ).execute()
                            break


                    time.sleep(1)
            return self.data_input
        except Exception as error:
            raise Exception("Erro ao verificar os dados de todos os envolvidos")