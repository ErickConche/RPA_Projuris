from modules.email.useCases.enviarEmail.main import EnviarEmail
from modules.email.useCases.fecharServerEmail.main import FecharServerEmail
import smtplib

class Email:
    
    def __init__(self) -> None:
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.server.login("yann.lima@docato.com.br", "yrifthtqfwugqefg")
    
    def enviarEmail(self,
                    body_envio):
        return EnviarEmail(body_envio=body_envio,
                           server=self.server).execute()
        
    def fecharServerEmail(self):
        return FecharServerEmail(server=self.server).execute()