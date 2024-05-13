import re


class ValidarHoraUseCase:
    def __init__(
        self,
        hora: str
    ) -> None:
        self.hora = hora

    def execute(self)->bool:
        try:
            padrao = r'^([01]?[0-9]|2[0-3]):([0-5][0-9])$'
            if re.match(padrao, self.hora):
                hora, minuto = map(int, self.hora.split(':'))
                if 0 <= hora <= 23 and 0 <= minuto <= 59:
                    return True
            return False
        except Exception as error:
            return False