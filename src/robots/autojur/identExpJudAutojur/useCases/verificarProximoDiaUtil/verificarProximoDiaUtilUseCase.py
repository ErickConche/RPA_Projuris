import datetime
import holidays

class VerificarProximoDiaUtilUseCase:
    def __init__(
        self,
        ano: int,
        mes: int,
        dia: int = 1
    ) -> None:
        self.ano = ano
        self.mes = mes
        self.dia = dia
        self.pais: str = "BR"
    

    def exec(self) -> str:
        """
        Retorna o próximo dia útil a partir da data dada (ano, mês, dia),
        considerando os finais de semana e feriados, porém não considera 
        """
        if self.dia < 1:
            raise ValueError("Data inválida!")
        try:
            feriados = holidays.country_holidays(self.pais, years=self.ano)
            data_inicial = datetime.date(self.ano, self.mes, self.dia)
            data_inicial += datetime.timedelta(days=1)
            while True:
                if data_inicial.weekday() < 5 and data_inicial not in feriados:
                    return data_inicial.strftime("%d/%m/%Y")
                data_inicial += datetime.timedelta(days=1)
        except Exception:
            ValueError("Data inválida!")