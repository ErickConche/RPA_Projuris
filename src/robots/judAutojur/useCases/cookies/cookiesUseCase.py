import pandas
import numpy
from robots.judAutojur.useCases.cookies.__model__.dadosCookiesModel import DadosCookiesModel

from robots.judAutojur.useCases.cookies.query.queryCookies import QueryCookies


class CookiesUseCase:
    def __init__(
        self,
        con_rd,
        idcliente: int
    ) -> None:
        self.con_rd = con_rd
        self.idcliente = idcliente

    def execute(self)->DadosCookiesModel:
        try:
            df = pandas.read_sql_query(QueryCookies(self.idcliente), con=self.con_rd)
            df = df.where(df.notnull(), None)
            df.replace({pandas.NaT: None}, inplace=True)
            df.replace({numpy.NaN: None}, inplace=True)
            df = df.to_dict(orient='records')
            if len(df)>0:
                data: DadosCookiesModel = DadosCookiesModel(
                    url=df[0].get("url"),
                    conteudo=df[0].get("conteudo"),
                )
                return data
            return None
        except Exception as error:
            raise error