
import numpy
import pandas
from models.cookies.__model__.dadosCookiesModel import DadosCookiesModel
from models.cookies.useCases.buscarCookiesUseCase.query.queryCookies import QueryCookies


class BuscarCookiesUseCase:
    def __init__(
        self,
        con_rd,
        queue: str,
        idcliente: int
    ) -> None:
        self.con_rd = con_rd
        self.idcliente = idcliente
        self.queue = queue

    def execute(self)->DadosCookiesModel:
        try:
            df = pandas.read_sql_query(QueryCookies(self.idcliente, self.queue), con=self.con_rd)
            df = df.where(df.notnull(), None)
            df.replace({pandas.NaT: None}, inplace=True)
            df.replace({numpy.NaN: None}, inplace=True)
            df = df.to_dict(orient='records')
            if len(df)>0:
                data: DadosCookiesModel = DadosCookiesModel(
                    url=df[0].get("url"),
                    conteudo=df[0].get("conteudo"),
                    session_cookie=df[0].get("session_cookie"),
                )
                return data
            return None
        except Exception as error:
            raise error