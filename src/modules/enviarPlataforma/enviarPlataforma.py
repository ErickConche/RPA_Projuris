
import json
import os
import time
from typing import List

import pika
from modules.logger.Logger import Logger


class EnviarPlataforma:
    def __init__(
        self,
        tenant:str,
        classLogger: Logger,
        data: dict,
        task_id:str,
        error: bool
    ) -> None:
        self.tenant = tenant
        self.data = data
        self.task_id = task_id
        self.classLogger = classLogger
        self.error = error

    def execute(self):
        data_return = {
            'TaskId':self.task_id,
            'Tenant': self.tenant,
            'ResultsFields': self.data,
            'Error':self.error
        }
        server_address = os.environ.get('RABBIT_CONNECTION')
        connection = pika.BlockingConnection(pika.URLParameters(server_address))
        channel = connection.channel()
        try:
            message = 'Enviando dados para fila do API-Gateway'
            self.classLogger.message(message=message)
            channel.basic_publish(
                exchange='', 
                routing_key='CuriosityConsumerSpt', 
                body=json.dumps(data_return,ensure_ascii=True).encode('utf8')
            )
            
        except Exception as error:
            pass
        time.sleep(1)
        channel.close()
        connection.close()
        