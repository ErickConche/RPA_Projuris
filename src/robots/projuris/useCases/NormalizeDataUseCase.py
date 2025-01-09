from datetime import datetime
import logging

class NormalizeDataUseCase:
    """
        Caso de uso para normalizar uma data recebida em formato de string.

        Esse caso de uso converte uma string de data no formato "YYYY/MM/DD" para "DD/MM/YYYY".
    """
    def __init__(self, date_received: str) -> None:
        """
            Inicializa a classe para normalizar a data recebida.
        """
        self.date_received = date_received


    def execute(date_received: str) -> str:
        """
            Normaliza a data recebida, convertendo o formato para "DD/MM/YYYY".

            Esse método verifica se a data recebida contém um separador 'T' ou um espaço em branco.
            Se contiver, a data é separada corretamente, e o formato é alterado. Caso contrário, a data é retornada no formato original.
        """
        try:
            date = ''
            # Se a data contiver o caractere 'T', o valor é dividido para pegar a parte da data
            date = date_received.split('T')[0].strip() if 'T' in date_received else date_received.split(' ')[0].strip()
            # Substitui o "-" por "/"
            date = date.replace("-", "/")
            # Divide a data em partes (ano, mês, dia)
            split_date = date.split('/')
            # Se o ano estiver na primeira posição (formato YYYY/MM/DD)
            if len(split_date[0]) == 4:
                # Converte a data para o formato "DD/MM/YYYY"
                date_obj = datetime.strptime(date, "%Y/%m/%d")
                date = date_obj.strftime("%d/%m/%Y")
            else:
                # Caso o formato da data já seja aceito, retorna a data sem alteração
                return date
        except Exception as e:
            logging.error(f'Data no formato incorreto: {e}')
            # Caso haja erro, a data será retornada como uma string vazia
            date = ''
        return date
