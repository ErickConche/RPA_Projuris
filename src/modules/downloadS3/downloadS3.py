
import json
import os
from random import randint
import time
from typing import List

import pika
import requests
from modules.logger.Logger import Logger


class DownloadS3:
    def __init__(
        self,
        url: str,
        complemento_nome: str = ''
    ) -> None:
        self.url = url
        self.complemento_nome = complemento_nome

    def execute(self):
        headers={
            'responseType': 'arraybuffer'
        }
        response = requests.get(url=self.url,headers=headers)
        infos_split = self.url.split("/")
        name_file = infos_split[len(infos_split)-1]
        posicao_do_ultimo_ponto = name_file.rfind('.')
        nome_arquivo_sem_extensao= name_file[:posicao_do_ultimo_ponto]
        extensao = name_file[posicao_do_ultimo_ponto + 1:]
        name_file = f"{nome_arquivo_sem_extensao}_{randint(50000,1000000)}.{extensao}"
        if self.complemento_nome != '':
            name_file = self.complemento_nome + '_'+ name_file
        open(name_file, "wb").write(response.content)
        return name_file