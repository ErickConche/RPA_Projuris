
import os
from random import randint
from typing import List
import zipfile

from modules.logger.Logger import Logger


class DescompactarZipUseCase:
    def __init__(
        self,
        name_file_zip:str,
        classLogger: Logger
    ) -> None:
        self.name_file_zip = name_file_zip
        self.classLogger = classLogger

    def execute(self)->List[str]:
        try:
            list_names = []
            with zipfile.ZipFile(self.name_file_zip, 'r') as zip_ref:
                nomes_arquivos = zip_ref.namelist()
                for nome_arquivo in nomes_arquivos:
                    # Lê o conteúdo do arquivo
                    conteudo_arquivo = zip_ref.read(nome_arquivo)
                    posicao_do_ultimo_ponto = nome_arquivo.rfind('.')
                    nome_arquivo_sem_extensao= nome_arquivo[:posicao_do_ultimo_ponto]
                    extensao = nome_arquivo[posicao_do_ultimo_ponto + 1:]
                    nome_arquivo = f"{nome_arquivo_sem_extensao}_{randint(50000,1000000)}.{extensao}"
                    # Salva o arquivo
                    with open(nome_arquivo, 'wb') as arquivo_destino:
                        arquivo_destino.write(conteudo_arquivo)
                    list_names.append(nome_arquivo)
            os.remove(self.name_file_zip)
            return list_names
        except Exception as error:
            message = f"Erro ao descompactar arquivos secundarios"
            self.classLogger.message(message)
            raise error