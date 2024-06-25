from time import sleep
from models.cookies.useCases.inserirCookieSessionUseCase.query.inserirCookieSessionQuery import InserirCookieSessionQuery


class InserirCookieSessionUseCase:
    
    def __init__(self,
                 con,
                 queue,
                 cookie_session,
                 idcliente):
        self.con = con
        self.cookie_session = cookie_session
        self.queue = queue
        self.idcliente = idcliente
        
    def execute(self):
        cont = 0
        qtde_tentativas = 0
        limite_tentativas = 10
        while cont == 0:
            try:
                cursor = self.con.cursor()
                cursor.execute(InserirCookieSessionQuery(self.queue, self.cookie_session, self.idcliente))
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
                