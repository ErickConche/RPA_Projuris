import time
import requests
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.__model__.PastaModel import PastaModel
from robots.legalone.judLegalone.useCases.validarPasta.validarPastaUseCase import ValidarPastaJudUseCase
from robots.legalone.judLegalone.useCases.inserirDadosEmpresa.inserirDadosEmpresaUseCase import InserirDadosEmpresaUseCase
from robots.legalone.judLegalone.useCases.inserirDadosEnvolvido.inserirDadosEnvolvidoUseCase import InserirDadosEnvolvidoUseCase
from robots.legalone.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel
from robots.legalone.judLegalone.useCases.inserirDadosAreaPrincipal.inserirDadosAreaPrincipalUseCase import InserirDadosAreaPrincipalUseCase
from robots.legalone.judLegalone.useCases.inserirDadosComplementares.inserirDadosComplementaresUseCase import InserirDadosComplementaresUseCase
from robots.legalone.judLegalone.useCases.inserirDadosPersonalizados.inserirDadosPersonalizadosUseCase import InserirDadosPersonalizadosUseCase
from robots.legalone.judLegalone.useCases.inserirDadosOutrosEnvolvidos.inserirDadosOutrosEnvolvidosUseCase import InserirDadosOutrosEnvolvidosUseCase


class CriarPastaCumprimentoSentencaUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger,
        context: BrowserContext,
        url_pasta_originaria:str
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.context = context
        self.url_pasta_originaria = url_pasta_originaria

    def execute(self)->PastaModel:
        try:
            cookies = self.context.cookies()
            cookies_str = ''
            for cookie in cookies:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            headers = {
                "X-Requested-With":"XMLHttpRequest",
                "Referer":self.url_pasta_originaria,
                "Host":"booking.nextlegalone.com.br",
                "Cookie":cookies_str
            }
            response = requests.get(url=self.url_pasta_originaria,headers=headers)
            site_html = BeautifulSoup(response.text, 'html.parser')
            commands = site_html.select(".command-add.command-link")
            url_pasta = None
            for command in commands:
                if command.text == 'Novo incidente':
                    link = command.attrs.get("href")
                    url_pasta = f"https://booking.nextlegalone.com.br{link}"
                    break

            self.page.goto(url_pasta)
            time.sleep(5)
            self.classLogger.message("Inserindo Outros envolvidos")
            InserirDadosOutrosEnvolvidosUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger,
                context=self.context
            ).execute()

            self.classLogger.message("Inserindo envolvidos")
            InserirDadosEnvolvidoUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger,
                context=self.context
            ).execute()
            
            self.classLogger.message("Inserindo dados principais")
            id_uf = InserirDadosAreaPrincipalUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger,
                context=self.context
            ).execute()

            self.classLogger.message("Inserindo dados da empresa")
            InserirDadosEmpresaUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger,
                context=self.context
            ).execute()

            self.classLogger.message("Inserindo dados complementares")
            InserirDadosComplementaresUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger,
                context=self.context,
                id_uf=id_uf
            ).execute()
            
            self.classLogger.message("Inserindo dados personalizados")
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
            time.sleep(5)

            response = ValidarPastaJudUseCase(
                page=self.page,
                nome_envolvido=self.data_input.nome_envolvido,
                processo=self.data_input.processo,
                processo_originario=self.data_input.processo_originario,
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