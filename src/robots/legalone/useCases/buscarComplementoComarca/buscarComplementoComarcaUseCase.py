import json
import time
import requests
from urllib.parse import urlencode
from modules.logger.Logger import Logger
from playwright.sync_api import BrowserContext
from robots.legalone.useCases.buscarDadosUfCidade.buscarDadosUfCidadeUseCase import BuscarDadosUfCidadeUseCase


class BuscarComplementoComarcaUseCase:
    def __init__(
        self,
        complemento_comarca: str,
        classLogger: Logger,
        id_comarca: int,
        id_uf: str,
        uf:str,
        nome_comarca: str,
        context: BrowserContext
    ) -> None:
        self.id_uf = id_uf
        self.uf = uf
        self.id_comarca = id_comarca
        self.nome_comarca = nome_comarca
        self.complemento_comarca = complemento_comarca
        self.classLogger = classLogger
        self.context = context

    def execute(self)->dict:
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = f"https://booking.nextlegalone.com.br/config/ComplementoForo/LookupComplementoForo?parentId={str(self.id_comarca)}&term={self.complemento_comarca}&pageSize=10&_=1707156417270"
            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":url,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }

            response = requests.get(url=url,headers=headers)

            json_response = json.loads(response.text)

            ### Insere os resultados no banco

            for row in json_response.get('Rows'):
                if row.get("Value") == self.complemento_comarca:
                    return row

            qtde_comarcas = json_response.get("Count")

            pages = qtde_comarcas//10
            if qtde_comarcas % 10 != 0:
                pages += 1
            
            cont = 1
            while cont < pages:
                url = f"https://booking.nextlegalone.com.br/config/ComplementoForo/LookupComplementoForo?parentId={str(self.id_comarca)}&term={self.complemento_comarca}&pageIndex={str(cont)}&pageSize=10&_=1707156417270"
                headers["Referer"] = url
                response = requests.get(url=url,headers=headers)

                json_response = json.loads(response.text)

                ### Insere os resultados no banco

                for row in json_response.get('Rows'):
                    if row.get("Value") == self.complemento_comarca:
                        return row

                time.sleep(0.5)
                cont +=1

            url = f"https://booking.nextlegalone.com.br/config/ComplementoForo/EditModal"

            uf_name = BuscarDadosUfCidadeUseCase(uf=self.uf,classLogger=self.classLogger,context=self.context).execute()

            body = urlencode({
                "JusticaText":"Justiça Estadual",
                "JusticaId":"13",
                "UFText":uf_name.get("UFText"),
                "UFId":uf_name.get("Id"),
                "ForoText":self.nome_comarca,
                "ForoId":self.id_comarca,
                "Descricao":self.complemento_comarca
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
                return json_response

            raise Exception ("O complemento da comarca não foi encontrado")
        except Exception as error:
            message = "Erro ao buscar o cadastro do complemento da comarca no Legalone"
            self.classLogger.message(message)
            raise error
        