from datetime import datetime

class FormatarDataUseCase:
    def __init__(
        self,
        data:str
    ) -> None:
        self.data = data

    def execute(self)->str:
        date_format = "%Y-%m-%d"
        if 'T' in self.data:
            self.data = self.data.split("T")[0]
            data_obj = datetime.strptime(self.data, date_format)
            self.data = data_obj.strftime("%d/%m/%Y")
        elif '-' in self.data:
            try:
                data_obj = datetime.strptime(self.data, date_format)
                self.data = data_obj.strftime("%d/%m/%Y")
            except Exception as error:
                raise Exception("Data invalida")
        return self.data