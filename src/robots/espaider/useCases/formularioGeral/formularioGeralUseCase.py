from datetime import datetime
from playwright.sync_api import Page
from robots.espaider.useCases.inserirDadosClassificacao.inserirDadosClassificacaoUseCase import (
    InserirDadosClassificacaoUseCase)
from modules.logger.Logger import Logger
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from robots.espaider.useCases.inserirDadosEmpresaGrupo.inserirDadosEmpresaGrupoUseCase import (
    InserirDadosEmpresaGrupoUseCase)
from robots.espaider.useCases.inserirPartesProcesso.inserirPartesProcessoUseCase import (
    InserirPartesProcessoUseCase)
from robots.espaider.useCases.inserirDadosDesdobramento.inserirDadosDesdobramentoUseCase import (
    InserirDadosDesdobramentoUseCase)
from robots.espaider.useCases.inserirDadosAssunto.inserirDadosAssuntoUseCase import (
    InserirDadosAssuntoUseCase)
from robots.espaider.useCases.inserirDadosPedidoPrincipal.inserirDadosPedidoPrincipalUseCase import (
    InserirDadosPedidoPrincipalUseCase)
from robots.espaider.useCases.inserirDadosPrognostico.inserirDadosPrognosticoUseCase import (
    InserirDadosPrognosticoUseCase)
from robots.espaider.useCases.inserirDadosMonetária.inserirDadosMonetáriaUseCase import (
    InserirDadosMonetáriaUseCase)
from robots.espaider.useCases.helpers.type_robot import is_autos, is_civel, is_cadastro
from robots.espaider.useCases.inserirDadosClassificacao.inserirDadosClassCadastroUseCase import (
    InserirDadosClassCadastroUseCase)

class FormularioGeralUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaEspaiderModel,
        classLogger: Logger,
        robot: str
    ):
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger
        self.robot = robot

    def execute(self):
        try:
            
            button = self.page.frame_locator('iframe').get_by_text("Novo")
            button.click()
            self.page.wait_for_load_state('load')
            
            self.page.wait_for_selector('iframe')
            frames = self.page.query_selector_all('iframe')
            
            if frames:
                last_frame = frames[-1]
                
                frame_name = last_frame.get_attribute('name')
                frame_id = last_frame.get_attribute('id')
                
                if frame_name or frame_id:
                    frame = self.page.frame(name=frame_name) if frame_name else self.page.frame(id=frame_id)
                    frame.wait_for_load_state("load")
            '''
            *** Informações Tópico Geral ***
            '''
            if is_cadastro(self.robot): 
                return InserirDadosClassCadastroUseCase(
                    page=self.page,
                    classLogger=self.classLogger,
                    data_input=self.data_input,
                    robot=self.robot,
                    iframe=frame
                ).execute()
            else:
                InserirDadosClassificacaoUseCase(
                    page=self.page,
                    frame=frame,
                    data_input=self.data_input, 
                    classLogger=self.classLogger
                ).execute()
                InserirDadosEmpresaGrupoUseCase(
                    page=self.page,
                    frame=frame,
                    data_input=self.data_input, 
                    classLogger=self.classLogger
                ).execute()
                InserirPartesProcessoUseCase(
                    page=self.page,
                    frame=frame,
                    data_input=self.data_input, 
                    classLogger=self.classLogger
                ).execute()
                InserirDadosDesdobramentoUseCase(
                    page=self.page,
                    frame=frame,
                    data_input=self.data_input, 
                    classLogger=self.classLogger
                ).execute()
                InserirDadosAssuntoUseCase(
                    page=self.page,
                    frame=frame,
                    data_input=self.data_input, 
                    classLogger=self.classLogger
                ).execute()
                if is_civel(self.robot):
                    InserirDadosPedidoPrincipalUseCase(
                        page=self.page,
                        frame=frame,
                        data_input=self.data_input, 
                        classLogger=self.classLogger
                    ).execute()

                '''
                *** Informações Tópico Valores | Prognóstico ***
                '''
                
                frame.wait_for_selector('button:has-text("Valores | Prognóstico")').click()
                frame.wait_for_timeout(2000)
                
                InserirDadosPrognosticoUseCase(
                    page=self.page,
                    frame=frame,
                    data_input=self.data_input, 
                    classLogger=self.classLogger
                ).execute()

                '''
                *** Informações Tópico Valores | Prognóstico ***
                '''
                if is_civel(self.robot):
                    frame.wait_for_selector('button:has-text("Atualização monetária")').click()
                    frame.wait_for_timeout(2000)

                    InserirDadosMonetáriaUseCase(
                        page=self.page,
                        frame=frame,
                        data_input=self.data_input, 
                        classLogger=self.classLogger
                    ).execute()

                '''
                *** Salvar cadastro principal ***
                '''

                frame.wait_for_selector('button:has-text("Geral")').click()
                frame.wait_for_timeout(2000)
                frame.wait_for_selector("#bm-Save").click()
                frame.wait_for_timeout(2000)

                pasta = frame.wait_for_selector("Pasta").inner_text()


                current_time = datetime.now().strftime("%d/%m/%Y")

                return {
                    "Pasta": pasta,
                    "Processo": self.data_input.processo,
                    "DataCadastro": current_time
                }
        except Exception as e:
            raise e