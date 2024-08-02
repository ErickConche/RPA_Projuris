import json
import time
from urllib.parse import urlencode
import requests
from unidecode import unidecode
from modules.logger.Logger import Logger
from playwright.sync_api import BrowserContext

from robots.legalone.judLegalone.useCases.deparas.deparas import Deparas
from robots.legalone.useCases.buscarDadosUfCidade.buscarDadosUfCidadeUseCase import BuscarDadosUfCidadeUseCase


class BuscarComarcaUseCase:
    def __init__(
        self,
        comarca: str,
        classLogger: Logger,
        id_uf: int,
        id_justica: int,
        context: BrowserContext,
        id_cidade: int,
        uf:str,
        cidade: str
    ) -> None:
        self.id_uf = id_uf
        self.uf = uf
        self.id_justica = id_justica
        self.comarca = comarca
        self.classLogger = classLogger
        self.context = context
        self.id_cidade = id_cidade
        self.cidade = cidade

    def execute(self)->dict:
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = f"https://booking.nextlegalone.com.br/config/Foro/LookupForo?idUF={str(self.id_uf)}&idJustica={str(self.id_justica)}&term={unidecode(self.comarca)}&pageSize=50&_=1706733430269"

            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":url,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }

            response = requests.get(url=url,headers=headers)

            json_response = json.loads(response.text)

            ### Insere os resultados no banco
            list_comarcas = []
            for row in json_response.get('Rows'):
                if unidecode(row.get("Value").upper()) == unidecode(self.comarca.upper()):
                    list_comarcas.append(row)

            qtde_comarcas = json_response.get("Count")

            pages = qtde_comarcas//50
            if qtde_comarcas % 50 != 0:
                pages += 1
            
            cont = 1
            while cont < pages:
                url = f"https://booking.nextlegalone.com.br/config/Foro/LookupForo?idUF={str(self.id_uf)}&pageIndex={str(cont)}&idJustica={str(self.id_justica)}&term={self.comarca}&pageSize=50&_=1706733430269"
                headers["Referer"] = url
                response = requests.get(url=url,headers=headers)

                json_response = json.loads(response.text)
                
                for row in json_response.get('Rows'):
                    if unidecode(row.get("Value").upper()) == unidecode(self.comarca.upper()):
                        list_comarcas.append(row)

                time.sleep(0.5)
                cont +=1
            
            if len(list_comarcas) > 0:
                return list_comarcas

            if not self.id_cidade:
                raise Exception ("Comarca e Cidade não encontradas")
            
            url = f"https://booking.nextlegalone.com.br/config/Foro/EditModal"

            body = urlencode({
                "HasFixedUf": "true",
                "JusticaText": Deparas.depara_id_justica(self.id_justica),
                "JusticaId": self.id_justica,
                "UFText": self.uf,
                "UFId": self.id_uf,
                "CityText": self.cidade,
                "CityId": self.id_cidade,
                "Nome": self.comarca
            })

            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":url,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str,
                "Content-Type":"application/x-www-form-urlencoded"
            }

            response = requests.post(url=url,data=body,headers=headers)
            json_response = json.loads(response.text)
            if response.status_code == 200:
                time.sleep(5)
                json_response['Value'] = json_response['Text']
                return [json_response]
            
            raise Exception ("Erro ao inserir Comarca")

        except Exception as error:
            message = "Erro ao buscar a comarca no Legalone"
            self.classLogger.message(message)
            raise error