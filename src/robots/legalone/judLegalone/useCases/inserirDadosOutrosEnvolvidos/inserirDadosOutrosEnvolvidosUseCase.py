import time
from bs4 import BeautifulSoup
from modules.logger.Logger import Logger
from playwright.sync_api import Page, BrowserContext
from robots.legalone.judLegalone.useCases.deparas.deparas import Deparas
from robots.legalone.useCases.buscarEnvolvido.buscarEnvolvidoUseCase import BuscarEnvolvidoUseCase
from robots.legalone.useCases.paginarElemento.paginarElementoUseCase import PaginarElementoUseCase
from robots.legalone.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class InserirDadosOutrosEnvolvidosUseCase:
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

    def execute(self):
        try:
            qtde_max = 10
            obj = self.data_input.__dict__
            index = 1
            elemento = self.page.locator('.edit-panel-wrapper:has-text("Outros envolvidos")')
            while index <= qtde_max:
                
                nome_envolvido = f"nome_outros_envolvidos{str(index)}"
                if obj.get(nome_envolvido) != '':
                    situacao = f"situacao_outros_envolvidos{str(index)}"
                    posicao = f"posicao_outros_envolvidos{str(index)}"
                    chave = f"cpf_cnpj_outros_envolvidos{str(index)}"

                    usuario = BuscarEnvolvidoUseCase(
                        nome_envolvido=obj.get(nome_envolvido),
                        cpf_cnpj_envolvido=obj.get(chave),
                        classLogger=self.classLogger,
                        context=self.context
                    ).execute()

                    nome_usuario = usuario.get("Text") if usuario.get("Text") else usuario.get("Value")

                    self.page.locator("#add_outro_envolvido").click()
                    time.sleep(5)
                    table = elemento.locator(".outros-envolvidos-list.edit-list")
                    li_table = table.locator(f'li:nth-child({str(index)})')
                    time.sleep(3)
                    site_html = BeautifulSoup(li_table.inner_html(), 'html.parser')
                    id_elemento = site_html.select_one("input").get("value").replace("-","_")

                    id_depara_situacao = Deparas.depara_situacao_outros_envolvidos(obj.get(situacao).strip())
                    select_elemento = li_table.locator('select')
                    select_elemento.select_option(value=f"{str(id_depara_situacao)}")
                    time.sleep(1)

                    id_elemento_posicao = f"#OutrosEnvolvidos_{id_elemento}__PosicaoEnvolvidoText"
                    id_elemento_nome = f"#OutrosEnvolvidos_{id_elemento}__EnvolvidoText"

                    li_table.locator(id_elemento_posicao).click()
                    time.sleep(1)
                    li_table.locator(id_elemento_posicao).type(obj.get(posicao))
                    time.sleep(3)
                    li_table.locator(id_elemento_posicao).press("Enter")
                    time.sleep(3)
                    elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
                    elemento_dropdown.locator(f'tr[data-val-id="{Deparas.depara_posicao_outros_envolvidos(obj.get(posicao))}"] td[data-val-field="Value"]:text("{obj.get(posicao)}")').click()
                    time.sleep(5)

                    li_table.locator(id_elemento_nome).click()
                    time.sleep(1)
                    li_table.locator(id_elemento_nome).type(nome_usuario)
                    time.sleep(3)
                    li_table.locator(id_elemento_nome).press("Enter")
                    time.sleep(3)
                    elemento_dropdown = self.page.locator('.lookup-dropdown[style*="display: block"]')
                    PaginarElementoUseCase(
                        page=self.page,
                        classLogger=self.classLogger,
                        context=self.context,
                        id_elemento=usuario.get("Id"),
                        valor_elemento=nome_usuario,
                        data_val_field='ContatoNome'
                    ).execute()
                    elemento_dropdown.locator(f'tr[data-val-id="{usuario.get("Id")}"] td[data-val-field="ContatoNome"]:text("{nome_usuario}")').click()
                    time.sleep(5)
                    
                    index += 1
                else:
                    break

            print("Finalizou")
        except Exception as error:
            raise Exception("Erro ao inserir os dados dos outros envolvidos")