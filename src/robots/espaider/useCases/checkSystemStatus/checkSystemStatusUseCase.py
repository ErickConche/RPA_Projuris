from modules.logger.Logger import Logger
from requests import Session


class CheckSystemStatusUseCase:
    def __init__(
        self,
        system_url: str,
        session: Session,
        classLogger: Logger
    ) -> None:
        self.session = session
        self.system_url = system_url
        self.classLogger = classLogger

    def execute(self):
        response = {
            "success":True,
        }
        
        try:
            self.classLogger.message('Validando status do sistema')
            status_response = self.session.get(f'{self.system_url}/@mvc/Modules/GetModules?', allow_redirects=True)
            if status_response.status_code < 302 and not 'errorTitle' in status_response.text:
                message = "Sistema está online"
                self.classLogger.message(message)
                return response
            raise Exception("Cookie expirado")
        except Exception as error:
            message = error.args[0]
            self.classLogger.message(message)
            response.update({
                "success": False,
                "message": message
            })
            return response
