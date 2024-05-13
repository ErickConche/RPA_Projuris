from bs4 import BeautifulSoup
from unidecode import unidecode
from modules.logger.Logger import Logger


class EncontrarTokenProcessoUseCase:
    def __init__(
        self,
        processo: str,
        trs: BeautifulSoup,
        classLogger: Logger
    ) -> None:
        self.classLogger = classLogger
        self.processo = processo.replace("-","").replace(".","")
        self.trs = trs

    def execute(self):
        try:
            data_rk = None
            for tr in self.trs:
                processo_encontrado = tr.select(".lg-dado")[4].next.replace("-","").replace(".","")
                if processo_encontrado == self.processo and not data_rk:
                    data_rk = tr.attrs.get("data-rk")
                    codigo_encontrado = tr.select('.lg-dado')[0].next
                    return data_rk, codigo_encontrado

                elif processo_encontrado == self.processo and data_rk:
                    message = f"O processo {self.processo} possui duas ou mais pastas cadastradas."
                    self.classLogger.message(message)
                    raise Exception (message)
        except Exception as error:
            message = f"Erro ao encontrar os tokens do processo"
            self.classLogger.message(message)
            raise error
    