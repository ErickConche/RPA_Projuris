import pandas
import numpy

from models.queues.useCases.buscarQueue.query.main import queryBuscarQueue

class BuscarQueue:
    
    def __init__(self,
                 con,
                 virtual_host,
                 queue):
        self.con = con
        self.virtual_host = virtual_host
        self.queue = queue
        
    def execute(self):
        try:
            df = pandas.read_sql_query(queryBuscarQueue(self.virtual_host,self.queue), con=self.con)
            df = df.where(df.notnull(), None)
            df.replace({pandas.NaT: None}, inplace=True)
            df.replace({numpy.NaN: None}, inplace=True)
            df = df.to_dict(orient='records')
            return df
        except Exception as error:
            raise error