import time
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.legalone.admLegalone.useCases.deparas.deparas import Deparas


class InserirDadosPersonalizadosUseCase:
    def __init__(
        self,
        page: Page,
        id_acomodacao:str,
        numero_reserva: str,
        nome_procon:str,
        numero_reclamacao: str,
        tiporeclamacao:str,
        tipoprocesso:str,
        dadosreserva:str,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.id_acomodacao = id_acomodacao
        self.numero_reserva = numero_reserva
        self.nome_procon = nome_procon
        self.numero_reclamacao = numero_reclamacao
        self.tiporeclamacao = tiporeclamacao
        self.tipoprocesso = tipoprocesso
        self.dadosreserva = dadosreserva
        self.classLogger = classLogger
    
    def execute(self):
        try:
            self.page.locator('label[data-collapsible-group-title="true"] >> text=Personalizados').click()
            time.sleep(4)
            self.page.query_selector('#IDDaAcomodacao_ServicoEntitySchema_p16887_o').click()
            time.sleep(1)
            self.page.query_selector('#IDDaAcomodacao_ServicoEntitySchema_p16887_o').type(self.id_acomodacao)
            time.sleep(1)
            self.page.query_selector('#NumeroDaReserva_ServicoEntitySchema_p16888_o').click()
            time.sleep(1)
            self.page.query_selector('#NumeroDaReserva_ServicoEntitySchema_p16888_o').type(self.numero_reserva)
            time.sleep(1)
            self.page.query_selector('#NomeDoPROCON_ServicoEntitySchema_p16889_o').click()
            time.sleep(1)
            self.page.query_selector('#NomeDoPROCON_ServicoEntitySchema_p16889_o').type(self.nome_procon)
            time.sleep(1)
            self.page.query_selector('#NumeroDaReclamacao_ServicoEntitySchema_p16890_o').click()
            time.sleep(1)
            self.page.query_selector('#NumeroDaReclamacao_ServicoEntitySchema_p16890_o').type(self.numero_reclamacao)
            time.sleep(1)


            self.page.query_selector('#TipoDaReclamacao_ServicoEntitySchema_p16891_o_Value').click()
            time.sleep(1)
            self.page.query_selector('#TipoDaReclamacao_ServicoEntitySchema_p16891_o_Value').type(self.tiporeclamacao)
            time.sleep(1)
            self.page.locator('#TipoDaReclamacao_ServicoEntitySchema_p16891_o_Lookup .lookup-button.lookup-filter').click()
            time.sleep(5)
            self.page.locator(f'tr[data-val-id="{Deparas.depara_tipo_reclamacao(self.tiporeclamacao)}"] td[data-val-field="Value"]:text("{self.tiporeclamacao}")').click()
            time.sleep(4)

            self.page.query_selector('#TipoDeProcesso_ServicoEntitySchema_p17570_o_Value').click()
            time.sleep(1)
            self.page.query_selector('#TipoDeProcesso_ServicoEntitySchema_p17570_o_Value').type(self.tipoprocesso)
            time.sleep(1)
            self.page.locator('#TipoDeProcesso_ServicoEntitySchema_p17570_o_Lookup .lookup-button.lookup-filter').click()
            time.sleep(5)
            self.page.locator(f'tr[data-val-id="{Deparas.depara_tipo_processo(self.tipoprocesso)}"] td[data-val-field="Value"]:text("{self.tipoprocesso}")').click()
            time.sleep(4)

            self.page.query_selector('#DemaisDadosReserva_ServicoEntitySchema_p17877_o').click()
            time.sleep(1)
            self.page.query_selector('#DemaisDadosReserva_ServicoEntitySchema_p17877_o').type(self.dadosreserva)
            time.sleep(1)
        except Exception as error:
            raise Exception("Erro ao inserir dados personalizados no formulario de criação")