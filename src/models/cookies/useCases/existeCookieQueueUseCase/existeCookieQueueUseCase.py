
import numpy
import pandas
from models.cookies.useCases.existeCookieQueueUseCase.query.queryCookies import ExisteCookieQueueQuery


class ExisteCookieQueueUseCase:
    def __init__(
        self,
        con_rd,
        queue: str,
        idcliente: int
    ) -> None:
        self.con_rd = con_rd
        self.queue = queue
        self.idcliente = idcliente

    def execute(self)->bool:
        try:
            df = pandas.read_sql_query(ExisteCookieQueueQuery(self.queue, self.idcliente), con=self.con_rd)
            df = df.where(df.notnull(), None)
            df.replace({pandas.NaT: None}, inplace=True)
            df.replace({numpy.NaN: None}, inplace=True)
            df = df.to_dict(orient='records')
            if len(df)>0:
                return True
            return False
        except Exception as error:
            raise error