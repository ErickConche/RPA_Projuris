import os
import zipfile
from typing import List
from random import randint
from unidecode import unidecode
from modules.formatacao.formatacao import Formatacao
from modules.logger.Logger import Logger
from modules.descompactarZip.__model__.ZipDescompactadoModel import ZipDescompactadoModel


class DescompactarZipUseCase:
    def __init__(
        self,
        name_file_zip:str,
        classLogger: Logger
    ) -> None:
        self.name_file_zip = name_file_zip
        self.classLogger = classLogger

    def execute(self)->List[ZipDescompactadoModel]:
        try:
            list_names = []
            with zipfile.ZipFile(self.name_file_zip, 'r') as zip_ref:
                nomes_arquivos = zip_ref.namelist()
                for nome_arquivo in nomes_arquivos:
                    # Lê o conteúdo do arquivo
                    conteudo_arquivo = zip_ref.read(nome_arquivo)
                    posicao_do_ultimo_ponto = nome_arquivo.rfind('.')
                    nome_arquivo_sem_extensao_sem_format = nome_arquivo[:posicao_do_ultimo_ponto]
                    nome_arquivo_sem_extensao= Formatacao().formatarNomeArquivo(nome_arquivo[:posicao_do_ultimo_ponto])
                    extensao = nome_arquivo[posicao_do_ultimo_ponto + 1:]
                    novo_nome_arquivo = f"{nome_arquivo_sem_extensao}_{randint(50000,1000000)}.{extensao}"
                    # Salva o arquivo
                    with open(novo_nome_arquivo, 'wb') as arquivo_destino:
                        arquivo_destino.write(conteudo_arquivo)
                    obj: ZipDescompactadoModel = ZipDescompactadoModel(
                        nome_original=nome_arquivo_sem_extensao,
                        novo_nome_arquivo=novo_nome_arquivo,
                        nome_original_sem_format=nome_arquivo_sem_extensao_sem_format
                    )
                    list_names.append(obj)
            os.remove(self.name_file_zip)
            return list_names
        except Exception as error:
            message = f"Erro ao descompactar arquivos secundarios"
            self.classLogger.message(message)
            raise error