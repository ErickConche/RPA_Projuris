
import json
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from models.cookies.cookiesUseCase import CookiesUseCase
from robots.autojur.identExpJudAutojur.useCases.validarEFormatarEntrada.__model__.dadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class ValidarEFormatarEntradaUseCase:
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

    def execute(self)-> DadosEntradaFormatadosModel:
        message = "Iniciando validação dos campos de entrada"
        self.classLogger.message(message)
        json_recebido:dict = json.loads(self.json_recebido)
        fields:dict = json_recebido.get("Fields")

        if not fields.get("Processo") or fields.get("Processo") is None:
            raise Exception("Informe o número do processo")
        if not fields.get("DataExpediente") or fields.get("DataExpediente") is None:
            raise Exception("Informe a data do expediente/audiência")
        if not fields.get("TipoExpediente") or fields.get("TipoExpediente") is None:
            raise Exception("Informe o tipo do expediente")
        
        usuario = "docato3"
        senha = "Docatoexpedientes3"

        message = (f"Usando o usuário {usuario} para login")
        self.classLogger.message(message)

        cookie = CookiesUseCase(
            con_rd=self.con_rd
        ).buscarCookies(
            queue="app-identificacao-exp-jud-autojur",
            idcliente=self.cliente.id
        )

        if not cookie:
            raise Exception("O sessão está expirada, favor entrar em contato do equipe de desenvolvimento para renovar sessão")
        
        data_input: DadosEntradaFormatadosModel = DadosEntradaFormatadosModel(
            username=usuario,
            password=senha,
            footprint=cookie.conteudo,
            url_cookie=cookie.url,
            processo=fields.get("Processo").strip(),
            data_expediente=fields.get("DataExpediente").strip(),
            tipo_expediente=fields.get("TipoExpediente").strip()
        )

        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)

        return data_input