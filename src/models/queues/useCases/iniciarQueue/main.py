from time import sleep
import pandas
import numpy

from models.queues.useCases.iniciarQueue.query.main import queryIniciarExecQueue



class IniciarExecQueue:
    
    def __init__(self,
                 con,
                 json_rec,
                 virtual_host,
                 queue):
        self.con = con
        self.json_rec = json_rec
        self.virtual_host = virtual_host
        self.queue = queue
        
    def execute(self):
        cont = 0
        qtde_tentativas = 0
        limite_tentativas = 10
        while cont == 0:
            try:
                cursor = self.con.cursor()
                cursor.execute(queryIniciarExecQueue(self.json_rec,self.virtual_host,self.queue))
                self.con.commit()
                cont = 1
                return
            except Exception as error:
                print("Error :"+str(error))
                self.con.rollback()
                qtde_tentativas = qtde_tentativas +1
                if qtde_tentativas >= limite_tentativas:
                    raise error
                sleep(5)
                