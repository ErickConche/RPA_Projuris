from models.cookies.useCases.buscarCookiesUseCase.buscarCookiesUseCase import BuscarCookiesUseCase
from models.cookies.useCases.existeCookieQueueUseCase.existeCookieQueueUseCase import ExisteCookieQueueUseCase
from models.cookies.useCases.alterarCookieSessionUseCase.alterarCookieSessionUseCase import AlterarCookieSessionUseCase
from models.cookies.useCases.inserirCookieSessionUseCase.inserirCookieSessionUseCase import InserirCookieSessionUseCase


class CookiesUseCase:
    def __init__(
        self,
        con_rd
    ) -> None:
        self.con_rd = con_rd

    def alterarCookieSession(self, queue, cookie_session):
        existeCookieQueue = ExisteCookieQueueUseCase(
            con_rd=self.con_rd,
            queue=queue
        ).execute()
        if existeCookieQueue:
            return AlterarCookieSessionUseCase(
                con=self.con_rd,
                queue=queue,
                cookie_session=cookie_session
            ).execute()
        return InserirCookieSessionUseCase(
            con=self.con_rd,
            queue=queue,
            cookie_session=cookie_session
        ).execute()
        
    def buscarCookies(self, queue, idcliente):
        return BuscarCookiesUseCase(
            con_rd=self.con_rd,
            queue=queue,
            idcliente=idcliente
        ).execute()