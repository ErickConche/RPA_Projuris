
class ExcecaoGeral(Exception):
    def __init__(self, log_erro, msg_erro: str = "SITE INDISPONÍVEL"):
        super().__init__(msg_erro)
        self.log_erro = log_erro
        self.msg_erro = msg_erro
