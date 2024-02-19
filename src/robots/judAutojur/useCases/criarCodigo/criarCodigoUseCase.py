import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.judAutojur.useCases.inserirDadosCadastrais.InserirDadosCadastraisUseCase import InserirDadosCadastraisUseCase
from robots.judAutojur.useCases.inserirDadosComentarios.inserirDadosComentariosUseCAse import InserirDadosComentariosUseCAse
from robots.judAutojur.useCases.inserirDadosEnvolvidos.inserirDadosEnvolvidosUseCase import InserirDadosEnvolvidosUseCase
from robots.judAutojur.useCases.inserirDadosOutrosEnvolvidos.inserirDadosOutrosEnvolvidosUseCase import InserirDadosOutrosEnvolvidosUseCase
from robots.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel
from robots.judAutojur.useCases.validarPastaAutojur.__model__.CodigoModel import CodigoModel
from robots.judAutojur.useCases.validarPastaAutojur.validarPastaAutojurUseCase import ValidarPastaAutojurUseCase

class CriarCodigoUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger,
        context: BrowserContext
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.context = context

    def execute(self)->CodigoModel:
        try:
            attemp = 0
            max_attemp = 3
            error_exec = None
            success = False
            while attemp < max_attemp:
                try:
                    self.page.goto("https://baz.autojur.com.br/sistema/processos/adicionar/novoProcesso.jsf?idTipoNovaPasta=5")
                    time.sleep(10)

                    InserirDadosOutrosEnvolvidosUseCase(
                        page=self.page,
                        data_input=self.data_input,
                        classLogger=self.classLogger
                    ).execute()
                
                    InserirDadosEnvolvidosUseCase(
                        page=self.page,
                        data_input=self.data_input,
                        classLogger=self.classLogger
                    ).execute()

                    InserirDadosCadastraisUseCase(
                        page=self.page,
                        data_input=self.data_input,
                        classLogger=self.classLogger
                    ).execute()

                    InserirDadosComentariosUseCAse(
                        page=self.page,
                        data_input=self.data_input,
                        classLogger=self.classLogger
                    ).execute()

                    ##Salvando codigo
                    self.page.locator('#btn-save\\:j_idt1131').click()
                    time.sleep(5)
                    response = ValidarPastaAutojurUseCase(
                        page=self.page,
                        pasta=self.data_input.pasta,
                        numero_reclamacao=self.data_input.numero_reclamacao,
                        classLogger=self.classLogger
                    ).execute()
                    if not response.codigo:
                        message = 'Erro ao inserir a pasta'
                        self.classLogger.message(message)
                        raise Exception (message)

                    message = "Pasta inserida, aguarde enquanto estamos pegando o codigo gerado"
                    self.classLogger.message(message)
                    attemp = max_attemp
                    success = True
                except Exception as error:
                    attemp +=1 
                    error_exec = error

            if not success:
                raise error_exec
            return response

        except Exception as error:
            raise error