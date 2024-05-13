import json


class FormatarArquivoUseCase:
    def __init__(
        self,
        arquivo:str
    ) -> None:
        self.arquivo = arquivo

    def execute(self)->str:
        if 'Url' in self.arquivo:
            arquivo_dict = json.loads(self.arquivo)
            if len(arquivo_dict) > 1:
                raise Exception("Foi informado mais de uma arquivo.")
            return arquivo_dict[0].get("ZipUrl")
        return self.arquivo