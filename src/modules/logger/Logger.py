

import os
import threading
import logging
import graypy

class Logger:

    def __init__(self,
                 hiring_id) -> None:
        self.hiring_ids: dict = {}
        self.call_ids: dict = {}
        self.prints: dict = {}
        self.hiring_ids[threading.current_thread().name] = hiring_id
        self.create_logger(hiring_id)
        self.hiring_id = hiring_id

    def create_logger(self,hiring_id: str):
        thread = threading.current_thread().name
        self.prints[thread] = logging.getLogger(hiring_id)
        self.prints[thread].setLevel(logging.DEBUG)
        if os.getenv('ENV') == 'production':
            graylog_ip = os.getenv('GRAYLOG_IP')
            graylog_port = int(os.getenv('GRAYLOG_PORT'))
            handler = graypy.GELFUDPHandler(graylog_ip, graylog_port)
            self.prints[thread].addHandler(handler)

    def create_default_logger(self,hiring_id: str):
        thread = threading.current_thread().name
        self.prints[thread] = logging.getLogger(hiring_id)
        self.prints[thread].setLevel(logging.DEBUG)

        handler = graypy.GELFUDPHandler('34.239.200.14', 12201)
        self.prints[thread].addHandler(handler)

    def set_hiring_id(self,hiring_id: str):
        self.hiring_ids[threading.current_thread().name] = hiring_id
        self.create_logger(hiring_id)

    def set_call_id(self,call_id: str):
        self.call_ids[threading.current_thread().name] = call_id

    def message(self,message: str):
        """
        Adiciona um mensagem os logs
        """
        print(message)
        thread = threading.current_thread().name
        final_message = f'{thread} - [{self.call_ids.get(thread)}] - '
        final_message += f'({self.hiring_ids.get(thread)}) - {message}\n'
        logger_print = self.prints.get(thread) or logging
        logger_print.info(final_message)