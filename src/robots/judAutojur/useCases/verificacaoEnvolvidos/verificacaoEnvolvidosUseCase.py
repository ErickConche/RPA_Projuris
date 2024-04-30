import json
import time
from urllib.parse import quote
from playwright.sync_api import Page, BrowserContext, sync_playwright
import requests
from unidecode import unidecode

from modules.logger.Logger import Logger
from robots.judAutojur.useCases.alterarObjetoEntrada.alterarObjetoEntradaUseCase import AlterarObjetoEntradaUseCase
from robots.judAutojur.useCases.buscarPessoa.buscarPessoaUseCase import BuscarPessoaUseCase
from robots.judAutojur.useCases.listarEnvolvidos.listarEnvolvidosUseCase import ListarEnvolvidosUseCase
from robots.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class VerificacaoEnvolvidosUseCase:
    def __init__(
        self,
        classLogger: Logger,
        data_input: DadosEntradaFormatadosModel,
        context: BrowserContext
    ) -> None:
        self.classLogger = classLogger
        self.context = context
        self.data_input = data_input

    def execute(self)->DadosEntradaFormatadosModel:
        try:
            lista_envolvidos = ListarEnvolvidosUseCase(
                classLogger=self.classLogger,
                data_input=self.data_input
            ).execute()
            for obj_envolvido in lista_envolvidos:
                envolvido = BuscarPessoaUseCase(
                    classLogger=self.classLogger,
                    context=self.context,
                    envolvido=obj_envolvido
                ).execute()
                self.data_input = AlterarObjetoEntradaUseCase(
                    data_input=self.data_input,
                    classLogger=self.classLogger,
                    envolvido=envolvido
                ).execute()
                time.sleep(0.5)
            return self.data_input
        except Exception as error:
            raise Exception("Erro ao verificar os dados de todos os envolvidos")