import time
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.espaider.__model__.CodigoModel import CodigoModel
from robots.espaider.useCases.pesquisarProcesso.pesquisarProcessoUseCase import PesquisarProcessoUseCase
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderCadastroModel import DadosEntradaEspaiderCadastroModel


class ValidarPastaEspaiderUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderCadastroModel,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self, attempt) -> CodigoModel:
        try:
            self.classLogger.message('Iniciando a validação da pasta')
            search_process_response = PesquisarProcessoUseCase(
                page=self.page,
                data_input=self.data_input,
                classLogger=self.classLogger
            ).execute()
            print(search_process_response)
            if not search_process_response.get('ProcessoEncontrado'):
                message = "O processo não foi cadastrado." if attempt == 2 else "O processo não está cadastrado, iniciando o cadastro."
                data_codigo: CodigoModel = CodigoModel(
                    found=False,
                    codigo=None,
                    iframe=search_process_response.get('Iframe')
                )
                self.classLogger.message(message)
            else:
                row = search_process_response.get('LinhaProcesso')
                headers = search_process_response.get('HeaderList')
                message = "O processo foi cadastrado."
                time.sleep(2)
                row_list = row.query_selector_all('td')
                header_dict = {}
                for idx, header in enumerate(headers):
                    print(header.inner_text())
                    header_dict.update({
                       header.inner_text():  idx
                    })
                data_codigo: CodigoModel = CodigoModel(
                    found=True,
                    codigo=row_list[header_dict['Pasta']].inner_text(),
                    data_cadastro=row_list[header_dict['Pré-cadastrado em']].inner_text()
                )
            self.classLogger.message(message)
            return data_codigo
        except Exception as error:
            print(str(error))
            raise Exception("Erro ao validar se a pasta já existe")
