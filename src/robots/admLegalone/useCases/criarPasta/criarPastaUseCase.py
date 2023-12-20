import time
from playwright.sync_api import Page, BrowserContext, sync_playwright

from modules.logger.Logger import Logger
from robots.admLegalone.useCases.inserirArquivos.inserirArquivosUseCase import InserirArquivosUseCase
from robots.admLegalone.useCases.inserirDadosEmpresa.inserirDadosEmpresaUseCase import InserirDadosEmpresaUseCase
from robots.admLegalone.useCases.inserirDadosEnvolvidos.inserirDadosEnvolvidosUseCase import InserirDadosEnvolvidosUseCase
from robots.admLegalone.useCases.inserirDadosObservacao.inserirDadosObservacaoUseCase import InserirDadosObservacaoUseCase
from robots.admLegalone.useCases.inserirDadosPersonalizados.inserirDadosPersonalizadosUseCase import InserirDadosPersonalizadosUseCase
from robots.admLegalone.useCases.inserirDadosPrincipais.inserirDadosPrincipaisUseCase import InserirDadosPrincipaisUseCase
from robots.admLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel
from robots.admLegalone.useCases.validarPasta.__model__.PastaModel import PastaModel
from robots.admLegalone.useCases.validarPasta.validarPastaUseCase import ValidarPastaUseCase

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
            self.page.goto("https://booking.nextlegalone.com.br/servicos/servicos/create?returnUrl=%2Fservicos%2Fservicos%2Fsearch%3Fajaxnavigation%3Dtrue")
            time.sleep(15)

            ## Inserindo dados no formulario
            InserirDadosPrincipaisUseCase(
                page=self.page,
                tipo_sistema=self.data_input.tipo_sistema,
                data_solicitacao=self.data_input.data_solicitacao,
                uf=self.data_input.uf,
                cidade=self.data_input.cidade,
                classLogger=self.classLogger,
                context=self.context
            ).execute()

            InserirDadosEnvolvidosUseCase(
                page=self.page,
                nome_envolvido=self.data_input.nome_envolvido,
                cpf_cnpj_envolvido=self.data_input.cpf_cnpj_envolvido,
                tipo_envolvido=self.data_input.tipo_envolvido,
                posicao_envolvido=self.data_input.posicao_envolvido,
                classLogger=self.classLogger,
                context=self.context
            ).execute()

            InserirDadosEmpresaUseCase(
                page=self.page,
                empresa=self.data_input.empresa,
                classLogger=self.classLogger
            ).execute()

            InserirDadosObservacaoUseCase(
                page=self.page,
                observacoes=self.data_input.observacoes,
                classLogger=self.classLogger
            ).execute()

            InserirDadosPersonalizadosUseCase(
                page=self.page,
                id_acomodacao=self.data_input.id_acomodacao,
                numero_reserva=self.data_input.numero_reserva,
                nome_procon=self.data_input.nome_procon,
                numero_reclamacao=self.data_input.numero_reclamacao,
                tiporeclamacao=self.data_input.tipo_reclamacao,
                tipoprocesso=self.data_input.tipo_processo,
                dadosreserva=self.data_input.dados_reserva,
                classLogger=self.classLogger
            ).execute()

            ## Salvando formulario
            self.page.click('button[name="ButtonSave"][value="0"]')
            time.sleep(15)

            message = "Pasta inserida. Aguarde enquanto buscamos o número gerado e fazemos o upload dos arquivos."
            self.classLogger.message(message)

            response = ValidarPastaUseCase(
                page=self.page,
                nome_envolvido=self.data_input.nome_envolvido,
                numero_reclamacao=self.data_input.numero_reclamacao,
                classLogger=self.classLogger
            ).execute()

            ###Inserir arquivos
            InserirArquivosUseCase(
                page=self.page,
                arquivo_principal=self.data_input.arquivo_principal,
                arquivos_secundarios=self.data_input.arquivos_secundarios,
                context=self.context,
                pasta=response.pasta,
                url_pasta=response.url_pasta,
                classLogger=self.classLogger
            ).execute()

            message = "Fim da execução da criação da pasta e upload dos arquivos"
            self.classLogger.message(message)

            
            return response
        except Exception as error:
            raise error