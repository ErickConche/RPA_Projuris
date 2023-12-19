
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
        url: str
    ) -> None:
        self.url = url

    def execute(self):
        headers={
            'responseType': 'arraybuffer'
        }
        response = requests.get(url=self.url,headers=headers)
        infos_split = self.url.split("/")
        name_file = infos_split[len(infos_split)-1]
        extension_file = name_file.split(".")[1]
        name_file = f'{name_file.split(".")[0]}_{randint(10000,5000000)}.{extension_file}'
        open(name_file, "wb").write(response.content)
        return name_file