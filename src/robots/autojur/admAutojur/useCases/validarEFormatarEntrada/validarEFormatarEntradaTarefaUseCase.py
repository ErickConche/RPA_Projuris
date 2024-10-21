
from datetime import datetime
import json
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from models.cookies.cookiesUseCase import CookiesUseCase
from robots.autojur.admAutojur.useCases.correcaoErrosUsuario.correcaoErrosUsuarioUseCase import CorrecaoErrosUsuarioUseCase
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaTarefaFormatadosModel import (
    DadosEntradaTarefaFormatadosModel)


class ValidarEFormatarEntradaTarefaUseCase:
    def __init__(
        self,
        classLogger: Logger,
        json_recebido:str,
        cliente:Cliente,
        con_rd,
    ) -> None:
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.cliente = cliente
        self.con_rd = con_rd

    def execute(self)-> DadosEntradaTarefaFormatadosModel:
        message = "Iniciando validação dos campos de entrada"
        self.classLogger.message(message)
        json_recebido:dict = json.loads(self.json_recebido)
        fields:dict = json_recebido.get("Fields")
        current_time = datetime.now()

        if not fields.get("Localizador"):
            raise Exception("Informe o localizador")
        
        if not fields.get("Conteudo"):
            raise Exception("Informe o conteúdo")
        
        usuario = "docato"
        senha = "Docato1234"

        message = (f"Usando o usuário {usuario} para login")
        self.classLogger.message(message)

        cookie = CookiesUseCase(
            con_rd=self.con_rd
        ).buscarCookies(
            queue="app-adm-autojur",
            idcliente=self.cliente.id
        )

        if not cookie:
            raise Exception("O sessão está expirada, favor entrar em contato do equipe de desenvolvimento para renovar sessão")
        
        data_input: DadosEntradaTarefaFormatadosModel = DadosEntradaTarefaFormatadosModel(
            username=usuario,
            password=senha,
            footprint=cookie.conteudo,
            url_cookie=cookie.url,
            conteudo=fields.get("Documento"),
            dados_busca=fields.get("Localizador"),
            evento=fields.get("Evento") or "DEFESA ADMINISTRATIVA",
            data=current_time.strftime("%d/%m/%Y"),
            hora=current_time.strftime("%H:%M"),
            responsavel="Thayse Simeão"
        )
        
        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)

        return data_input