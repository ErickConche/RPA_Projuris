import os
from dotenv import load_dotenv
load_dotenv()
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class EnviarEmail:
    
    def __init__(self,
                 body_envio,
                 server) -> None:
        self.body_envio = body_envio
        self.server = server
    
    def execute(self):
        sender = "yann.lima@docato.com.br"
        recipients = self.body_envio['para']
        msg = MIMEMultipart()
        msg['Subject'] = self.body_envio['assunto']
        msg['From'] = sender
        msg['To'] = ', '.join(recipients) 
        
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(self.body_envio['data'], "rb").read())
        encoders.encode_base64(part)
        
        part.add_header('Content-Disposition', 'attachment; filename="'+self.body_envio['nome_arquivo']+'"')
        
        msg.attach(MIMEText(self.body_envio['texto'], 'plain'))
        msg.attach(part)
        
        self.server.sendmail(sender, recipients, msg.as_string())
        
        return 