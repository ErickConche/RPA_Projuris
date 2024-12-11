import time
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from global_variables.open_modal_partes_autojur import get_opened_modal, update_opened_modal
from robots.autojur.admAutojur.useCases.validarPastaAutojur.__model__.CodigoModel import CodigoModel
from robots.autojur.admAutojur.useCases.inserirArquivos.inserirArquivosUseCase import InserirArquivosUseCase
from robots.autojur.admAutojur.useCases.validarPastaAutojur.validarPastaAutojurUseCase import ValidarPastaAutojurUseCase
from robots.autojur.admAutojur.useCases.inserirDadosCadastrais.InserirDadosCadastraisUseCase import InserirDadosCadastraisUseCase
from robots.autojur.admAutojur.useCases.inserirDadosEnvolvidos.inserirDadosEnvolvidosUseCase import InserirDadosEnvolvidosUseCase
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel
from robots.autojur.admAutojur.useCases.inserirDadosPersonalizados.inserirDadosPersonalizadosUseCase import InserirDadosPersonalizadosUseCase


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
            max_attemp = 1
            error_exec = None
            success = False
            while attemp < max_attemp:
                try:
                    self.page.goto("https://baz.autojur.com.br/sistema/processos/adicionar/novoProcesso.jsf?idTipoNovaPasta=3")
                    time.sleep(5)
                    if get_opened_modal():
                        while get_opened_modal():
                            time.sleep(3)
                            print('Aguardando outra execução finalizar o cadastro das partes envolvidas')
                        InserirDadosEnvolvidosUseCase(
                            page=self.page,
                            data_input=self.data_input,
                            classLogger=self.classLogger
                        ).execute()
                    else:
                        update_opened_modal(True)
                        InserirDadosEnvolvidosUseCase(
                            page=self.page,
                            data_input=self.data_input,
                            classLogger=self.classLogger
                        ).execute()
                        update_opened_modal(False)

                    self.classLogger.message("Inserindo dados cadastrais")
                    InserirDadosCadastraisUseCase(
                        page=self.page,
                        data_input=self.data_input,
                        classLogger=self.classLogger
                    ).execute()

                    self.classLogger.message("Inserindo dados personalizados")
                    InserirDadosPersonalizadosUseCase(
                        page=self.page,
                        data_input=self.data_input,
                        classLogger=self.classLogger
                    ).execute()

                    self.classLogger.message("Inserindo arquivo")
                    InserirArquivosUseCase(
                        page=self.page,
                        data_input=self.data_input,
                        classLogger=self.classLogger
                    ).execute()

                    ##Salvando codigo
                    self.page.query_selector('div>div>a:has-text(" Salvar")').click()
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
            update_opened_modal(False)
            raise error