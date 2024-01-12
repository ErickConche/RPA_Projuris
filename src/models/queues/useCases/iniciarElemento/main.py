from time import sleep
import pandas
import numpy

from models.queues.useCases.iniciarElemento.query.main import queryIniciarElementoExecQueue


class IniciarElementoQueue:
    
    def __init__(self,
                 con,
                 id):
        self.con = con
        self.id = id
        
    def execute(self):
        cont = 0
        qtde_tentativas = 0
        limite_tentativas = 10
        while cont == 0:
            try:
                cursor = self.con.cursor()
                cursor.execute(queryIniciarElementoExecQueue(id=self.id))
                self.con.commit()
                cont = 1
                qtde_linhas = cursor.rowcount
                return qtde_linhas
            except Exception as error:
                print("Error :"+str(error))
                self.con.rollback()
                qtde_tentativas = qtde_tentativas +1
                if qtde_tentativas >= limite_tentativas:
                    raise error
                sleep(5)
                