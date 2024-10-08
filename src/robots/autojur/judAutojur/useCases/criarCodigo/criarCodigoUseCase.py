import time
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.autojur.__model__.CodigoModel import CodigoModel
from robots.autojur.judAutojur.useCases.validarPastaAutojur.validarPastaAutojurUseCase import ValidarPastaAutojurUseCase
from robots.autojur.judAutojur.useCases.inserirDadosCadastrais.InserirDadosCadastraisUseCase import InserirDadosCadastraisUseCase
from robots.autojur.judAutojur.useCases.inserirDadosEnvolvidos.inserirDadosEnvolvidosUseCase import InserirDadosEnvolvidosUseCase
from robots.autojur.judAutojur.useCases.inserirDadosComentarios.inserirDadosComentariosUseCAse import InserirDadosComentariosUseCAse
from robots.autojur.judAutojur.useCases.inserirDadosResponsavel.inserirDadosResponsavelUseCase import InserirDadosResponsavelUseCase
from robots.autojur.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel
from robots.autojur.judAutojur.useCases.inserirDadosOutrosEnvolvidos.inserirDadosOutrosEnvolvidosUseCase import InserirDadosOutrosEnvolvidosUseCase


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

    def execute(self) -> CodigoModel:
        try:
            attemp = 0
            max_attemp = 1
            error_exec = None
            success = False
            while attemp < max_attemp:
                try:
                    url = "https://baz.autojur.com.br/sistema/processos/adicionar/novoProcesso.jsf?idTipoNovaPasta=5"
                    self.page.goto(url)
                    time.sleep(5)

                    self.classLogger.message("Inserindo Outros envolvidos")
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

                    self.classLogger.message("Inserindo dados cadastrais")
                    InserirDadosCadastraisUseCase(
                        page=self.page,
                        data_input=self.data_input,
                        classLogger=self.classLogger
                    ).execute()

                    self.classLogger.message("Inserindo dados responsável")
                    InserirDadosResponsavelUseCase(
                        page=self.page,
                        data_input=self.data_input,
                        classLogger=self.classLogger
                    ).execute()

                    self.classLogger.message("Inserindo comentarios")
                    InserirDadosComentariosUseCAse(
                        page=self.page,
                        data_input=self.data_input,
                        classLogger=self.classLogger
                    ).execute()

                    # Salvando codigo
                    self.page.query_selector('[id="btn-save"]>div>div>a:has-text(" Salvar")').click()
                    time.sleep(5)
                    if self.page.query_selector('[id="confirm-alteracao-numero-processo-originario"]').is_visible():
                        print('EXIBIU MODAL PROCESSO ORIGINÁRIO')
                        self.page.query_selector('[id="confirm-alteracao-numero-processo-originario"]>div>div>div>a').click()
                        time.sleep(3)
                    response = ValidarPastaAutojurUseCase(
                        page=self.page,
                        pasta=self.data_input.pasta,
                        processo=self.data_input.processo,
                        classLogger=self.classLogger,
                        context=self.context
                    ).execute()
                    if not response.codigo:
                        message = 'Erro ao inserir a pasta'
                        self.classLogger.message(message)
                        raise Exception(message)

                    message = "Pasta inserida, aguarde enquanto estamos pegando o codigo gerado"
                    self.classLogger.message(message)
                    attemp = max_attemp
                    success = True
                except Exception as error:
                    attemp += 1
                    error_exec = error

            if not success:
                raise error_exec
            return response

        except Exception as error:
            raise error
