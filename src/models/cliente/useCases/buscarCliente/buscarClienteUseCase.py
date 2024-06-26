from typing import List
import pandas
import numpy
from models.cliente.__model__.ClienteModel import ClienteModel
from models.cliente.useCases.buscarCliente.query.buscarClienteQuery import BuscarClienteQuery



class BuscarClienteUseCase:
    def __init__(
        self,
        con,
        tenant:str
    ) -> None:
        self.con = con
        self.tenant = tenant

    def execute(self)->ClienteModel:
        try:
            df = pandas.read_sql_query(BuscarClienteQuery(self.tenant), con=self.con)
            df = df.where(df.notnull(), None)
            df.replace({pandas.NaT: None}, inplace=True)
            df.replace({numpy.NaN: None}, inplace=True)
            df = df.to_dict(orient='records')
            return_sistem: ClienteModel = ClienteModel(
                id=df[0]['id'],
                nome=df[0]['nome'],
                tenant=df[0]['tenant'],
                config_add=df[0]['config_add'],
                base_url=df[0]['base_url']
            )
            return return_sistem
        except Exception as error:
            raise error
