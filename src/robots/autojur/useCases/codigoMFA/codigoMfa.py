from imbox import Imbox
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger


class codigoMfa:
    def __init__(
        self,
        username: str,
        classLogger: Logger
    ) -> None:
        self.email = 'yann.lima@docato.com.br'
        self.password_email = 'zipwpizyxkujquuc'
        self.username = username
        self.classLogger = classLogger

    def execute(self):
        try:
            user_on_email = ''.join([i for i in self.username if not i.isdigit()]).upper() + " " + ''.join([i for i in self.username if i.isdigit()])
            with Imbox('imap.gmail.com', username=self.email, password=self.password_email) as imbox:
                unread_messages = imbox.messages(unread=True, sent_from='noreply@perceptvision.com.br')
                for uid, message in unread_messages:
                    email_html = BeautifulSoup(message.raw_email, 'html.parser')
                    user_email = email_html.select_one('tr>td>p').text
                    user_email = user_email.split(' - ')[0]
                    if 'Tentativa de login em um novo dispositivo' in message.subject and user_on_email == user_email:
                        codigo = email_html.select_one('tr>td>div').text
                        if codigo:
                            imbox.mark_seen(uid)
                            return codigo.strip()
        except Exception as error:
            raise Exception("Erro ao pegar o código MFA do email")
