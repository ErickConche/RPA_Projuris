from bs4 import BeautifulSoup
from unidecode import unidecode
from modules.logger.Logger import Logger
from robots.expJudAutojur.useCases.acessarProcesso.acessarProcessoUseCase import AcessarProcessoUseCase


class EncontrarTokenProcessoUseCase:
    def __init__(
        self,
        processo: str,
        trs: BeautifulSoup,
        classLogger: Logger,
        view_state: str,
        url: str,
        headers: dict
    ) -> None:
        self.classLogger = classLogger
        self.processo = processo.replace("-","").replace(".","").strip()
        self.trs = trs
        self.view_state = view_state
        self.url = url
        self.headers = headers

    def execute(self):
        try:
            data_rk = None
            count = 0
            for tr in self.trs:
                processo_encontrado = tr.select(".lg-dado")[4].next.replace("-","").replace(".","").strip()
                data_rk = tr.attrs.get("data-rk")
                if processo_encontrado == '':
                    processo_encontrado = AcessarProcessoUseCase(
                        view_state=self.view_state,
                        url=self.url,
                        headers=self.headers,
                        data_rk=data_rk,
                        classLogger=self.classLogger
                    ).execute()
                if processo_encontrado == self.processo:
                    count += 1
                    codigo_encontrado = tr.select('.lg-dado')[0].next

                if processo_encontrado == self.processo and count > 1:
                    message = f"O processo {self.processo} possui duas ou mais pastas cadastradas."
                    self.classLogger.message(message)
                    raise Exception (message)
            return data_rk, codigo_encontrado
        except Exception as error:
            message = f"Erro ao encontrar os tokens do processo"
            self.classLogger.message(message)
            raise error
    