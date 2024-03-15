
from modules.formatacao.useCases.formatarCpfCnpjUseCase import FormatarCpfCnpjUseCase
from modules.formatacao.useCases.formatarDataUseCase import FormatarDataUseCase


class Formatacao:
    def __init__(
        self,
    ) -> None:
        pass

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