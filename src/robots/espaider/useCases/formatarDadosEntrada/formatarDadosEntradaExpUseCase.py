import json
from modules.logger.Logger import Logger
from models.cookies.cookiesUseCase import CookiesUseCase
from models.cliente.__model__.ClienteModel import ClienteModel
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderExpModel import (
    DadosEntradaEspaiderExpModel)
from modules.decodePassword.decodePassword import DecodePassword

class FormatarDadosEntradaExpUseCase:
    def __init__(
        self,
        classLogger: Logger,
        json_recebido: str,
        client: ClienteModel,
        con_rd,
        queue,
        robot
    ) -> None:
        self.cliente = client
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.con_rd = con_rd
        self.robot = robot
        self.queue = queue

    def execute(self) -> DadosEntradaEspaiderExpModel:
        json_recebido: dict = json.loads(self.json_recebido)
        fields: dict = json_recebido.get("Fields")
        credentials: dict = json_recebido.get('Credentials')

        data_input: DadosEntradaEspaiderExpModel = DadosEntradaEspaiderExpModel(
            cookie_session="",
            username=credentials.get("Username"),
            password=DecodePassword(classLogger=self.classLogger, password=credentials.get("Password")).decrypt(),
            data_expediente=fields.get("DataExpediente"),
            processo=fields.get("Processo"),
            andamento=fields.get("Andamento"),
            complementos=fields.get("Complementos") if fields.get("Complementos") else None,
            compromisso=fields.get("Compromisso") if fields.get("Compromisso") else None,
            data_audiencia=fields.get("DataAudiencia") if fields.get("DataAudiencia") else None,
            hora_audiencia=fields.get("HoraAudiencia") if fields.get("HoraAudiencia") else None,
        )

        cookie = CookiesUseCase(
            con_rd=self.con_rd
        ).buscarCookies(
            queue=self.queue,
            idcliente=self.cliente.id
        )

        if cookie:
            data_input.cookie_session = cookie.session_cookie

        return data_input