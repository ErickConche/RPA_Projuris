
import json
from datetime import datetime
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from models.cookies.cookiesUseCase import CookiesUseCase
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaTarefaFormatadosModel import (
    DadosEntradaTarefaFormatadosModel)


class ValidarEFormatarEntradaTarefaUseCase:
    def __init__(
        self,
        classLogger: Logger,
        json_recebido: str,
        cliente: Cliente,
        con_rd,
    ) -> None:
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.cliente = cliente
        self.con_rd = con_rd

    def execute(self) -> DadosEntradaTarefaFormatadosModel:
        message = "Iniciando validação dos campos de entrada"
        self.classLogger.message(message)
        json_recebido: dict = json.loads(self.json_recebido)
        fields: dict = json_recebido.get("Fields")
        current_time = datetime.now()

        if not fields.get("Localizador"):
            raise Exception("Informe o localizador")

        if not fields.get("Documento"):
            raise Exception("Informe o conteúdo")

        # Atualizar após a migration subir pra produção
        # if not fields.get("Evento"):
        #     raise Exception("Informe o evento")
        
        # if not fields.get("Responsavel"):
        #     raise Exception("Informe o responsável")

        usuario = "docato3"
        senha = "Docatoexpedientes3"

        message = (f"Usando o usuário {usuario} para login")
        self.classLogger.message(message)

        cookie = CookiesUseCase(
            con_rd=self.con_rd
        ).buscarCookies(
            queue="app-adm-tarefa-autojur",
            idcliente=self.cliente.id
        )

        if not cookie:
            raise Exception("O sessão está expirada, favor entrar em contato do equipe de desenvolvimento para renovar sessão")

        data_input: DadosEntradaTarefaFormatadosModel = DadosEntradaTarefaFormatadosModel(
            username=usuario,
            password=senha,
            cookie_session=cookie.session_cookie,
            footprint=cookie.conteudo,
            url_cookie=cookie.url,
            conteudo=fields.get("Documento"),
            dados_busca=fields.get("Localizador"),
            evento=fields.get("Evento") or "DEFESA ADMINISTRATIVA",
            # evento=fields.get("Evento") if fields.get("Evento") else "",
            data=current_time.strftime("%d/%m/%Y"),
            hora=current_time.strftime("%H:%M"),
            # responsavel=fields.get("Responsavel") if fields.get("Responsavel") else ""
            responsavel="Bruno Medeiros Gonçalves da Silva"
        )

        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)
        return data_input
