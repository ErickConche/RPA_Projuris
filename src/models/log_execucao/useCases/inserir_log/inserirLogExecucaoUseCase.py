from time import sleep
from models.log_execucao.useCases.inserir_log.query.inserirLogExecucaoQuery import InserirLogExecucaoQuery


class InserirLogExecucaoUseCase:
    def __init__(
        self,
        con,
        queue_execucao:str,
        protocolo1_recebido:str,
        protocolo2_recebido:str,
        protocolo_enviado:str
    ) -> None:
        self.con = con
        self.queue_execucao = queue_execucao
        self.protocolo1_recebido = protocolo1_recebido
        self.protocolo2_recebido = protocolo2_recebido
        self.protocolo_enviado = protocolo_enviado

    def execute(self):
        cont = 0
        qtde_tentativas = 0
        limite_tentativas = 10
        while cont == 0:
            try:
                cursor = self.con.cursor()
                query = InserirLogExecucaoQuery(
                    self.queue_execucao,
                    self.protocolo1_recebido,
                    self.protocolo2_recebido,
                    self.protocolo_enviado
                )
                cursor.execute(query)
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
                
