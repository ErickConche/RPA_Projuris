from typing import List
import pandas
import numpy
from models.cliente.__model__.ClienteModel import ClienteModel
from models.cliente.useCases.buscarCliente.query.buscarClienteQuery import BuscarClienteQuery
from models.log_execucao.__model__.LogExecucaoModel import LogExecucaoModel
from models.log_execucao.useCases.buscar_log.query.buscarLogQuery import buscarLogQuery



class BuscarLogUseCase:
    def __init__(
        self,
        con,
        queue:str,
        protocolo1_recebido:str,
        protocolo2_recebido: str
    ) -> None:
        self.con = con
        self.queue = queue
        self.protocolo1_recebido = protocolo1_recebido
        self.protocolo2_recebido = protocolo2_recebido

    def execute(self)->LogExecucaoModel:
        try:
            df = pandas.read_sql_query(buscarLogQuery(
                self.queue,
                self.protocolo1_recebido,
                self.protocolo2_recebido
            ), con=self.con)
            df = df.where(df.notnull(), None)
            df.replace({pandas.NaT: None}, inplace=True)
            df.replace({numpy.NaN: None}, inplace=True)
            df = df.to_dict(orient='records')
            if len(df)>0:
                return_sistem: LogExecucaoModel = LogExecucaoModel(
                    id=df[0]['id'],
                    queue_execucao=df[0]['queue_execucao'],
                    protocolo1_recebido=df[0]['protocolo1_recebido'],
                    protocolo2_recebido=df[0]['protocolo2_recebido'],
                    protocolo_enviado=df[0]['protocolo_enviado'],
                    data_envio=df[0]['data_envio']
                )
                return return_sistem
            else:
                return None
        except Exception as error:
            raise error
