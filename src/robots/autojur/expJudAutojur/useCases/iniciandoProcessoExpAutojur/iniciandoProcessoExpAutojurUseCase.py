import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from modules.logger.Logger import Logger
from robots.autojur.expJudAutojur.useCases.criarTarefa.criarTarefaUseCase import CriarTarefaUseCase
from robots.autojur.expJudAutojur.useCases.validarTarefas.validarTarefasUseCase import ValidarTarefasUseCase
from robots.autojur.expJudAutojur.useCases.buscarProcesso.buscarProcessoUseCase import BuscarProcessoUseCase
from robots.autojur.expJudAutojur.useCases.acessarAgendamentos.acessarAgendamentosUseCase import AcessarAgendamentosUseCase
from robots.autojur.expJudAutojur.useCases.encontrarTokenProcesso.encontrarTokenProcessoUseCase import EncontrarTokenProcessoUseCase
from robots.autojur.expJudAutojur.useCases.iniciandoProcessoExpAutojur.__model__.CodigoModel import CodigoModel, InfosRequisicaoModel
from robots.autojur.expJudAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class IniciandoProcessoExpAutojurUseCase:
    def __init__(
        self,
        classLogger: Logger,
        data_input: DadosEntradaFormatadosModel,
        cookies: str
    ) -> None:
        self.classLogger = classLogger
        self.cookies = cookies
        self.data_input = data_input

    def execute(self)->CodigoModel:
        try:
            message = f"Iniciando a execução do processo {self.data_input.processo}"
            self.classLogger.message(message=message)
            url = "https://baz.autojur.com.br/sistema/processos/processo.jsf"
            headers = {
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Cookie":self.cookies
            }
            response = requests.get(url=url, headers=headers)
            site_html = BeautifulSoup(response.text, 'html.parser')
            view_state = site_html.select_one("#form-pesquisa").find('input', {'name': 'javax.faces.ViewState'}).attrs.get('value')
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

            trs = BuscarProcessoUseCase(
                view_state=view_state,
                headers=headers,
                url=url,
                classLogger=self.classLogger,
                processo=self.data_input.processo
            ).execute()

            if trs[0].text == 'Nenhum registro encontrado':
                message = f"Não foi encontrado nenhum cadastro para o processo {self.data_input.processo}"
                self.classLogger.message(message)
                raise Exception (message)
            
            data_rk, codigo_encontrado = EncontrarTokenProcessoUseCase(
                processo=self.data_input.processo,
                trs=trs,
                classLogger=self.classLogger,
                view_state=view_state,
                headers=headers,
                url=url
            ).execute()

            site_html, existem_tarefas = AcessarAgendamentosUseCase(
                view_state=view_state,
                headers=headers,
                url=url,
                data_rk=data_rk,
                classLogger=self.classLogger
            ).execute()

            tarefa_existe = False
            if existem_tarefas:
                tarefa_existe = ValidarTarefasUseCase(
                    evento=self.data_input.evento,
                    site_html=site_html,
                    classLogger=self.classLogger
                ).execute()

                if tarefa_existe:
                    data_codigo: CodigoModel = CodigoModel(
                        found=True,
                        codigo="Já Cadastrado"
                    )
                    return data_codigo

            message = f"Processo: {self.data_input.processo}.Não existe nenhum lançamento com menos de 7 dias para esse evento."
            self.classLogger.message(message)

            body = urlencode({
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "btnAcoes:btnAddTarefa",
                "javax.faces.partial.execute": "@all",
                "btnAcoes:btnAddTarefa": "btnAcoes:btnAddTarefa",
                "btnAcoes": "btnAcoes",
                "javax.faces.ViewState": view_state
            })

            response = requests.post(url=url, data=body, headers=headers)

            text = BeautifulSoup(response.text, 'html.parser').select_one("eval").next
            pfdlgcid = re.search(r"pfdlgcid:'(.*?)'", text).group(1).replace("\\","")
            uuid_processo = re.search(r"uuidProcesso=(.*?)'", text).group(1).replace("\\","")
            url_tarefa = f"https://baz.autojur.com.br/sistema/mdAdicionarTarefa.jsf?uuidProcesso={uuid_processo}&pfdlgcid={pfdlgcid}"
            url_tarefa_post = f"https://baz.autojur.com.br/sistema/mdAdicionarTarefa.jsf?pfdlgcid={pfdlgcid}"

            infos_requisicao = InfosRequisicaoModel(
                url=url_tarefa,
                url_post=url_tarefa_post,
                headers=headers,
                pfdlgcid=pfdlgcid,
                uuid_processo=uuid_processo,
                view_state=view_state,
                url_processo=url
            )

            CriarTarefaUseCase(
                data_input=self.data_input,
                classLogger=self.classLogger,
                infos_requisicao=infos_requisicao
            ).execute()

            body = urlencode({
                "javax.faces.partial.ajax": "true",
                "javax.faces.source": "btnAcoes:btnAddTarefa",
                "javax.faces.partial.execute": "btnAcoes:btnAddTarefa",
                "javax.faces.behavior.event": "dialogReturn",
                "javax.faces.partial.event": "dialogReturn",
                "btnAcoes:btnAddTarefa_pfdlgcid": pfdlgcid,
                "btnAcoes": "btnAcoes",
                "javax.faces.ViewState": view_state
            })

            headers['X-Requested-With'] = 'XMLHttpRequest'

            response = requests.post(url=url, data=body, headers=headers)

            if 'Operação efetuada com sucesso.  Foi cadastrado 1 registro' in response.text:
                message = f"Tarefa inserida com sucesso para o processo {self.data_input.processo}"
                self.classLogger.message(message)
                data_codigo: CodigoModel = CodigoModel(
                    found=True,
                    codigo=codigo_encontrado
                )
                return data_codigo
            raise Exception("Erro ao inserir pasta")
        
        except Exception as error:
            raise Exception(str(error))
        
