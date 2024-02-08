import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.judLegalone.useCases.inserirDadosAreaPrincipal.inserirDadosAreaPrincipalUseCase import InserirDadosAreaPrincipalUseCase
from robots.judLegalone.useCases.inserirDadosComplementares.inserirDadosComplementaresUseCase import InserirDadosComplementaresUseCase
from robots.judLegalone.useCases.inserirDadosEmpresa.inserirDadosEmpresaUseCase import InserirDadosEmpresaUseCase
from robots.judLegalone.useCases.inserirDadosEnvolvido.inserirDadosEnvolvidoUseCase import InserirDadosEnvolvidoUseCase
from robots.judLegalone.useCases.inserirDadosOutrosEnvolvidos.inserirDadosOutrosEnvolvidosUseCase import InserirDadosOutrosEnvolvidosUseCase
from robots.judLegalone.useCases.inserirDadosPersonalizados.inserirDadosPersonalizadosUseCase import InserirDadosPersonalizadosUseCase
from robots.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel
from robots.judLegalone.useCases.validarPasta.__model__.PastaModel import PastaModel
from robots.judLegalone.useCases.validarPasta.validarPastaUseCase import ValidarPastaJudUseCase

class CriarPastaIndenizatoriaUseCase:
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

    def execute(self)->PastaModel:
        try:
            self.page.goto("https://booking.nextlegalone.com.br/processos/processos/create?returnUrl=%2Fhome%2Findex")
            time.sleep(15)

            InserirDadosOutrosEnvolvidosUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger,
                context=self.context
            ).execute()

            InserirDadosEnvolvidoUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger,
                context=self.context
            ).execute()
            
            id_uf = InserirDadosAreaPrincipalUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger,
                context=self.context
            ).execute()

            InserirDadosEmpresaUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger,
                context=self.context
            ).execute()

            InserirDadosComplementaresUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger,
                context=self.context,
                id_uf=id_uf
            ).execute()
            
            InserirDadosPersonalizadosUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger,
                context=self.context
            ).execute()

            ## Salvando formulario
            try:
                self.page.query_selector('button[name="ButtonSave"][value="0"]').click()
            except Exception as error:
                pass
            time.sleep(15)

            response = ValidarPastaJudUseCase(
                page=self.page,
                nome_envolvido=self.data_input.nome_envolvido,
                processo=self.data_input.processo,
                classLogger=self.classLogger,
                context=self.context
            ).execute()
            
            if not response.pasta:
                message = "Erro ao criar pasta"
                self.classLogger.message(message)
                raise Exception("Erro ao criar pasta")
            
            return response

        except Exception as error:
            raise error