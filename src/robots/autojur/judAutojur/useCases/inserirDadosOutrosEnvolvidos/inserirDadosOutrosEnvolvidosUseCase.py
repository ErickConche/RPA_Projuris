import time
from bs4 import BeautifulSoup
from unidecode import unidecode
from playwright.sync_api import Page
from modules.logger.Logger import Logger
from robots.autojur.judAutojur.useCases.deparas.deparas import Deparas
from robots.autojur.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel

class InserirDadosOutrosEnvolvidosUseCase:
    def __init__(
        self,
        page: Page,
        data_input: DadosEntradaFormatadosModel,
        classLogger: Logger
    ) -> None:
        self.page = page
        self.data_input = data_input
        self.classLogger = classLogger

    def execute(self):
        try:
            qtde_max = 10
            obj = self.data_input.__dict__
            index = 1
            
            time.sleep(5)
            while index <= qtde_max:
                
                nome = f"nome_outros_envolvidos{str(index)}"
                if obj.get(nome) != '':
                    posicao = f"posicao_outros_envolvidos{str(index)}"
                    chave = f"cpf_cnpj_outros_envolvidos{str(index)}"
                    nome_envolvido = obj.get(nome)

                    has_cpf_cnpj = True  if obj.get(chave) != '' else False

                    self.page.locator("#painel-envolvidos\\:form-outros-envolvidos\\:btn-adicionar-envolvido-outros").click()
                    time.sleep(5)
                    site_html = BeautifulSoup(self.page.content(), 'html.parser')
                    url_iframe = f"https://baz.autojur.com.br{site_html.select_one('iframe').attrs.get('src')}"
                    frame = self.page.frame(url=url_iframe)
                    if has_cpf_cnpj:
                        frame.locator('button[data-id="form-pesquisa-pessoa:componente-pesquisa-pessoa:cmb-campo-pesquisa-rapida"]').click()
                        time.sleep(5)
                        frame.locator('#form-pesquisa-pessoa\\:componente-pesquisa-pessoa\\:campo .bs-searchbox input').type("CPF/CNPJ")
                        time.sleep(1)
                        frame.locator('li:has-text("CPF/CNPJ")').click()
                        time.sleep(5)
                        frame.fill('#form-pesquisa-pessoa\\:componente-pesquisa-pessoa\\:txt-conteudo',obj.get(chave))
                        time.sleep(3)
                    else: 
                        frame.fill('#form-pesquisa-pessoa\\:componente-pesquisa-pessoa\\:txt-conteudo',obj.get(nome))
                        time.sleep(3)
                    frame.locator('button[data-id="form-pesquisa-pessoa:cmbCategoriaPessoa"]').click()
                    time.sleep(5)
                    frame.locator('li:has-text("Todos")').click()
                    time.sleep(5)
                    
                    frame.locator("#form-pesquisa-pessoa\\:componente-pesquisa-pessoa\\:btn-pesquisar").click()
                    time.sleep(10)
                    frame.locator("#form-pesquisa-pessoa\\:ativo").click()
                    time.sleep(1)

                    site_html = BeautifulSoup(frame.content(), 'html.parser')

                    trs = site_html.select_one("#form-pesquisa-pessoa\\:tabela_data").select("tr")
                    codigo = None
                    time.sleep(5)
                    if trs[0].text == 'Nenhum registro encontrado':
                        frame.locator("#form-pesquisa-pessoa\\:j_idt91").click()
                        time.sleep(5)
                        site_html = BeautifulSoup(self.page.content(), 'html.parser')
                        url_iframe = f"https://baz.autojur.com.br{site_html.select('iframe')[1].attrs.get('src')}"
                        frame = self.page.frame(url=url_iframe)
                        frame.locator("#form-tipo-pessoa\\:ff-nome\\:nome").click()
                        time.sleep(5)
                        frame.locator("#form-tipo-pessoa\\:ff-nome\\:nome").type(obj.get(nome))
                        time.sleep(5)
                        if len(obj.get(chave)) >14:
                            frame.locator("#form-tipo-pessoa\\:j_idt26\\:tipo\\:1").click()
                            time.sleep(1)
                        if frame.locator("#modal-duplicados").is_visible():
                            frame.locator("#modal-duplicados .ui-commandlink.ui-widget.btn.btn-default").click()
                            time.sleep(3)
                        frame.fill('#form-tipo-pessoa\\:ff-cpf-cnpj\\:j_idt29',obj.get(chave))
                        time.sleep(5)
                        if frame.locator("#modal-duplicados").is_visible():
                            frame.locator("#modal-duplicados .ui-commandlink.ui-widget.btn.btn-default").click()
                            time.sleep(3)
                        frame.locator("#form-salvar-pessoa\\:j_idt662").click()
                        time.sleep(5)
                    
                    else:
                        for tr in trs:
                            tds = tr.select("td")
                            if has_cpf_cnpj and tds[7].text == obj.get(chave):
                                codigo = tds[1].text
                                nome_envolvido = tds[3].previous
                                break
                                
                            elif unidecode(tds[3].previous.upper()) == unidecode(nome_envolvido.upper()):
                                codigo = tds[1].text
                                break
                        if not codigo:
                            frame.locator("#form-pesquisa-pessoa\\:j_idt91").click()
                            time.sleep(3)
                            site_html = BeautifulSoup(self.page.content(), 'html.parser')
                            url_iframe = f"https://baz.autojur.com.br{site_html.select('iframe')[1].attrs.get('src')}"
                            frame = self.page.frame(url=url_iframe)
                            frame.locator("#form-tipo-pessoa\\:ff-nome\\:nome").click()
                            time.sleep(1)
                            frame.locator("#form-tipo-pessoa\\:ff-nome\\:nome").type(nome_envolvido)
                            time.sleep(3)
                            if len(obj.get(chave)) >14:
                                frame.locator("#form-tipo-pessoa\\:j_idt26\\:tipo\\:1").click()
                                time.sleep(1)
                            if frame.locator("#modal-duplicados").is_visible():
                                frame.locator("#modal-duplicados .ui-commandlink.ui-widget.btn.btn-default").click()
                                time.sleep(3)
                            frame.fill('#form-tipo-pessoa\\:ff-cpf-cnpj\\:j_idt29',obj.get(chave))
                            time.sleep(5)
                            if frame.locator("#modal-duplicados").is_visible():
                                frame.locator("#modal-duplicados .ui-commandlink.ui-widget.btn.btn-default").click()
                                time.sleep(3)
                            frame.fill('#form-tipo-pessoa\\:ff-cpf-cnpj\\:j_idt29',obj.get(chave))
                            time.sleep(3)
                            frame.locator("#form-salvar-pessoa\\:j_idt662").click()
                            time.sleep(5)
                        else:
                            frame.locator(f'tr[data-rk="{codigo}"]').click()
                            time.sleep(1)
                            frame.locator("#form-pesquisa-pessoa\\:btn-selecionar").click()
                            time.sleep(5)

                    self.page.locator("#j_idt1257\\:form-envolvidos\\:ff-qualificacao\\:autocomplete_input").click()
                    time.sleep(1)
                    self.page.locator("#j_idt1257\\:form-envolvidos\\:ff-qualificacao\\:autocomplete_input").type(obj.get(posicao))
                    time.sleep(1)
                    self.page.locator(f'li[data-item-value="{Deparas.depara_posicao(obj.get(posicao))}"]').click()
                    time.sleep(1)

                    self.page.locator("#j_idt1257\\:form-envolvidos\\:btn-salvar-envolvido").click()
                    time.sleep(10)
                    index += 1
                else:
                    break

            print("Finalizou")

        except Exception as error:
            message = "Erro ao inserir dados dos outros envolvidos"
            self.classLogger.message(message)
            raise Exception ("Erro ao inserir dos outros envolvidos")