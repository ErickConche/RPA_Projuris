from typing import List
from models.queues.useCases.buscarQueue.main import BuscarQueue
from models.queues.useCases.finalizarQueue.main import FinalizarExecQueue
from models.queues.useCases.iniciarQueue.main import IniciarExecQueue

class QueueExecucao:
    
    def __init__(self,
                 con) -> None:
        self.con = con
        
    def buscarQueue(self,virtual_host,queue):
        return BuscarQueue(con=self.con,virtual_host=virtual_host,queue=queue).execute()
    
    def finalizarExecQueue(self,id):
        return FinalizarExecQueue(con=self.con,id=id).execute()
    
    def iniciarExecQueue(self,json_rec,virtual_host,queue):
        return IniciarExecQueue(con=self.con,json_rec=json_rec,virtual_host=virtual_host,queue=queue).execute()