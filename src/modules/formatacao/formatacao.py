
from modules.formatacao.useCases.formatarArquivoUseCase import FormatarArquivoUseCase
from modules.formatacao.useCases.formatarCpfCnpjUseCase import FormatarCpfCnpjUseCase
from modules.formatacao.useCases.formatarDataUseCase import FormatarDataUseCase
from modules.formatacao.useCases.formatarNomeArquivo import FormatarNomeArquivo


class Formatacao:
    def __init__(
        self,
    ) -> None:
        pass

    def formatarNomeArquivo(
        self,
        nome_arquivo: str
    ):
        return FormatarNomeArquivo(nome_arquivo=nome_arquivo).execute()

    def formatarArquivo(
        self,
        arquivo: str
    ):
        return FormatarArquivoUseCase(arquivo=arquivo).execute()

    def formatarCpfCnpj(
        self,
        cpf_cnpj:str
    )->str:
        return FormatarCpfCnpjUseCase(cpf_cnpj=cpf_cnpj).execute()

    def formatarData(
        self,
        data:str
    )->str:
        return FormatarDataUseCase(data=data).execute()