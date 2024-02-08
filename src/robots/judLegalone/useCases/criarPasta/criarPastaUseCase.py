import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.judLegalone.useCases.criarPastaIndenizatoria.criarPastaIndenizatoriaUseCase import CriarPastaIndenizatoriaUseCase
from robots.judLegalone.useCases.inserirArquivos.inserirArquivosUseCase import InserirArquivosUseCase
from robots.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel
from robots.judLegalone.useCases.validarPasta.__model__.PastaModel import PastaModel

class CriarPastaUseCase:
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
            if self.data_input.titulo == 'Indenizatória':
                response = CriarPastaIndenizatoriaUseCase(
                    page=self.page,
                    data_input=self.data_input,
                    classLogger=self.classLogger,
                    context=self.context
                ).execute()
                
            
            InserirArquivosUseCase(
                page=self.page,
                arquivo_principal=self.data_input.arquivo_principal,
                context=self.context,
                pasta=response.pasta,
                url_pasta=response.url_pasta,
                classLogger=self.classLogger,
                processo=self.data_input.processo
            ).execute()

            return response

            
        except Exception as error:
            raise error