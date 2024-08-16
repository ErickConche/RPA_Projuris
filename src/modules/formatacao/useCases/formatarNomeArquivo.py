from unidecode import unidecode

class FormatarNomeArquivo:
    def __init__(
        self,
        nome_arquivo: str
    ) -> None:
        self.nome_arquivo = nome_arquivo

    def execute(self):
        return unidecode(self.nome_arquivo.replace(" ","_"))