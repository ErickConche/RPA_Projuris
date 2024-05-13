from time import sleep
from models.cookies.useCases.alterarCookieSessionUseCase.query.alterarCookieSessionQuery import AlterarCookieSessionQuery


class AlterarCookieSessionUseCase:
    
    def __init__(self,
                 con,
                 queue,
                 cookie_session):
        self.con = con
        self.cookie_session = cookie_session
        self.queue = queue
        
    def execute(self):
        cont = 0
        qtde_tentativas = 0
        limite_tentativas = 10
        while cont == 0:
            try:
                cursor = self.con.cursor()
                cursor.execute(AlterarCookieSessionQuery(self.queue, self.cookie_session))
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
                