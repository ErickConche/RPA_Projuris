import base64
from modules.logger.Logger import Logger


class DecodePassword:

    def __init__(
        self,
        classLogger: Logger,
        password: str
    ):
        self.classLogger = classLogger
        self.passwordEncrypted = password

    def decrypt(self):
        passDecoded = ""
        try:
            passDecoded = base64.b64decode(self.passwordEncrypted)
        except:
            print('Senha não esta encriptada, não foi possivel decodificar!')   
            passDecoded = self.passwordEncrypted
        finally:
            return passDecoded