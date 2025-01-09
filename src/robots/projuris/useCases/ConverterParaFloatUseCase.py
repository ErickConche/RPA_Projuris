class ConverterParaFloatUseCase:
    """
    Caso de uso para converter um valor em string para um número do tipo float.

    Essa classe garante que, caso a conversão falhe, será retornado o valor padrão 0.0.
    """

    def __init__(self, value: str) -> None:
        """
        Inicializa a classe com o valor a ser convertido.
        """
        self.value = value

    def execute(self) -> float:
        """
        Executa a conversão do valor para float.
        """
        try:
            return float(self.value)
        except ValueError:
            # Retorna 0.0 se o valor não puder ser convertido
            return 0.0
