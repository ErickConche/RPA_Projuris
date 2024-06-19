class ModularizarData:
    def __init__(
        self,
        data_1: str,
        data_2: str
    ) -> None:
        self.data_1 = data_1
        self.data_2 = data_2

    def execute(
        self
    ):
        try:
            data_1_possui_hora = True if len(self.data_1.split()) > 1 else False
            data_2_possui_hora = True if len(self.data_2.split()) > 1 else False
            if data_1_possui_hora and not data_2_possui_hora:
                self.data_2 = f"{self.data_2} {self.data_1.split()[1]}"
            
            elif not data_1_possui_hora and data_2_possui_hora:
                self.data_1 = f"{self.data_1} {self.data_2.split()[1]}"

            return self.data_1, self.data_2
        except Exception as error:
            raise Exception("Erro ao modularizar datas")