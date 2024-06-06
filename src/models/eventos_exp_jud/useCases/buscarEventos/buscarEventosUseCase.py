
from typing import List
import numpy
import pandas
from models.eventos_exp_jud.__model__.dadosEventosModel import DadosEventosModel
from models.eventos_exp_jud.useCases.buscarEventos.query.queryEventos import QueryEventos


class BuscarEventosUseCase:
    def __init__(
        self,
        con_rd
    ) -> None:
        self.con_rd = con_rd

    def execute(self)->List[DadosEventosModel]:
        try:
            df = pandas.read_sql_query(QueryEventos(), con=self.con_rd)
            df = df.where(df.notnull(), None)
            df.replace({pandas.NaT: None}, inplace=True)
            df.replace({numpy.NaN: None}, inplace=True)
            df = df.to_dict(orient='records')
            list_events: List[DadosEventosModel] = []
            if len(df)>0:
                for row in df:
                    data: DadosEventosModel = DadosEventosModel(
                        nome_evento=row.get("nome_evento"),
                        id_evento=row.get("id_evento"),
                        usa_hora=row.get("usa_hora"),
                    )
                    list_events.append(data)
                return list_events
            return None
        except Exception as error:
            raise error