

import os
import threading
import logging
import graypy

class Logger:

    def __init__(self,
                 hiring_id) -> None:
        Logger.hiring_ids[threading.current_thread().name] = hiring_id
        Logger.create_logger(hiring_id)
        self.hiring_id = hiring_id

    hiring_ids: dict = {}
    call_ids: dict = {}
    prints: dict = {}

    def create_logger(hiring_id: str):
        thread = threading.current_thread().name
        Logger.prints[thread] = logging.getLogger(hiring_id)
        Logger.prints[thread].setLevel(logging.DEBUG)
        if os.getenv('ENV') == 'production':
            graylog_ip = os.getenv('GRAYLOG_IP')
            graylog_port = int(os.getenv('GRAYLOG_PORT'))
            handler = graypy.GELFUDPHandler(graylog_ip, graylog_port)
            Logger.prints[thread].addHandler(handler)

    def create_default_logger(hiring_id: str):
        thread = threading.current_thread().name
        Logger.prints[thread] = logging.getLogger(hiring_id)
        Logger.prints[thread].setLevel(logging.DEBUG)

        handler = graypy.GELFUDPHandler('34.239.200.14', 12201)
        Logger.prints[thread].addHandler(handler)

    def set_hiring_id(hiring_id: str):
        Logger.hiring_ids[threading.current_thread().name] = hiring_id
        Logger.create_logger(hiring_id)

    def set_call_id(call_id: str):
        Logger.call_ids[threading.current_thread().name] = call_id

    def message(self,message: str):
        """
        Adiciona um mensagem os logs
        """
        print(message)
        thread = threading.current_thread().name
        final_message = f'{thread} - [{Logger.call_ids.get(thread)}] - '
        final_message += f'({Logger.hiring_ids.get(thread)}) - {message}\n'
        logger_print = Logger.prints.get(thread) or logging
        logger_print.info(final_message)

    def error(error_message: str):
        """
        Adiciona um mensagem de erro os logs
        """
        thread = threading.current_thread().name
        final_message = f'{thread} - [{Logger.call_ids.get(thread)}] - '
        final_message += f'({Logger.hiring_ids.get(thread)}) - {error_message}'
        logger_print = Logger.prints.get(thread) or logging
        logger_print.error(final_message)

    def success(sucess_message: str):
        """
        Adiciona um mensagem de sucesso os logs
        """
        thread = threading.current_thread().name
        final_message = f'{thread} - [{Logger.call_ids.get(thread)}] - '
        final_message += f'({Logger.hiring_ids.get(thread)}) - {sucess_message}'
        logger_print = Logger.prints.get(thread) or logging
        logger_print.info(final_message)

    def alert(alert_message: str):
        """
        Adiciona um mensagem de alerta os logs
        """
        thread = threading.current_thread().name
        final_message = f'{thread} - [{Logger.call_ids.get(thread)}] - '
        final_message += f'({Logger.hiring_ids.get(thread)}) - {alert_message}'
        logger_print = Logger.prints.get(thread) or logging
        logger_print.warning(final_message)
