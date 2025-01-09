class NormalizeValorUseCase:
    """
        Caso de uso para normalizar e converter valores monetários.

        Esta classe é responsável por normalizar uma string de valor monetário, removendo símbolos como 'R$' e 'RS', 
        substituindo vírgulas por pontos e convertendo o valor em um número de ponto flutuante. O valor final é retornado
        no formato monetário, com duas casas decimais, separado por vírgulas.
    """

    def __init__(self, valor: str) -> None:
        """
            Inicializa o caso de uso com o valor monetário fornecido.
        """
        self.valor = valor
        self.valor_float = 0.0
        
    def execute(self) -> str:
        """
            Executa a normalização e conversão do valor monetário.

            Este método remove os símbolos de moeda (como 'R$' e 'RS'), substitui os pontos por nada e as vírgulas por pontos
            para garantir que o valor seja interpretado corretamente como um número de ponto flutuante. O valor resultante
            é formatado para exibição como uma string monetária com duas casas decimais, com o separador de milhar como ponto
            e o separador decimal como vírgula.
        """
        self.valor = self.valor.replace('R$', '').replace('RS', '').replace('.', '').replace(',', '.').strip()
        self.valor_float = float(self.valor)
        return f"{self.valor_float:,.2f}".replace('.', ',').replace(',', '.', 1)

    def __str__(self) -> str:
        """
            Retorna o valor monetário como uma string formatada.

            Este método converte o valor em ponto flutuante para uma string formatada com separadores de milhar e decimal
            de acordo com o padrão monetário brasileiro.
        """
        return f"{self.valor_float:,.2f}".replace('.', ',').replace(',', '.', 1)
