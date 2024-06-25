from typing import Optional
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.__model__.PastaModel import PastaModel
from robots.legalone.judLegalone.useCases.inserirArquivos.inserirArquivosUseCase import InserirArquivosUseCase
from robots.legalone.judLegalone.useCases.criarPastaIndenizatoria.criarPastaIndenizatoriaUseCase import CriarPastaIndenizatoriaUseCase
from robots.legalone.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel
from robots.legalone.judLegalone.useCases.criarPastaCumprimentoSentenca.criarPastaCumprimentoSentencaUseCase import CriarPastaCumprimentoSentencaUseCase


class CriarPastaUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger,
        context: BrowserContext,
        url_pasta_originaria: Optional[str] = None
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.context = context
        self.url_pasta_originaria = url_pasta_originaria

    def execute(self)->PastaModel:
        try:
            if self.data_input.titulo == 'Indenizatória' or self.data_input.titulo == 'Reclamação Pré-Processual':
                response = CriarPastaIndenizatoriaUseCase(
                    page=self.page,
                    data_input=self.data_input,
                    classLogger=self.classLogger,
                    context=self.context
                ).execute()

            elif self.data_input.titulo == 'Cumprimento de Sentença' or self.data_input.titulo == 'Carta Precatória':
                response = CriarPastaCumprimentoSentencaUseCase(
                    page=self.page,
                    data_input=self.data_input,
                    classLogger=self.classLogger,
                    context=self.context,
                    url_pasta_originaria=self.url_pasta_originaria
                ).execute()
            else:
                raise Exception("O titulo passado não foi mapeado")
            InserirArquivosUseCase(
                arquivo_principal=self.data_input.arquivo_principal,
                context=self.context,
                url_pasta=response.url_pasta,
                classLogger=self.classLogger,
                processo=self.data_input.processo
            ).execute()

            return response
            
        except Exception as error:
            raise error