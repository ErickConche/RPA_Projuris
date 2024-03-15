from datetime import datetime

class FormatarDataUseCase:
    def __init__(
        self,
        data:str
    ) -> None:
        self.data = data

    def execute(self)->str:
        if 'T' in self.data:
            self.data = self.data.split("T")[0]
            data_obj = datetime.strptime(self.data, "%Y-%m-%d")
            self.data =  data_obj.strftime("%d/%m/%Y")
        return self.data