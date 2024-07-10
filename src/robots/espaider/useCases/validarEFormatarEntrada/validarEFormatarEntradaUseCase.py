from typing import Union
from modules.logger.Logger import Logger
from robots.espaider.useCases.validarDadosEntrada.validarDadosEntradaUseCase import (
    ValidarDadosEntradaUseCase)
from robots.espaider.useCases.formatarDadosEntrada.formatarDadosEntradaUseCase import (
    FormatarDadosEntradaUseCase)
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from models.cliente.__model__.ClienteModel import ClienteModel
from robots.espaider.useCases.validarDadosEntrada.validarDadosEntradaExpUseCase import (
    ValidarDadosEntradaExpUseCase)
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderExpModel import (
    DadosEntradaEspaiderExpModel)
from robots.espaider.useCases.formatarDadosEntrada.formatarDadosEntradaExpUseCase import (
    FormatarDadosEntradaExpUseCase)


class ValidarEFormatarEntradaUseCase:
    def __init__(
        self,
        classLogger: Logger,
        json_recebido: str,
        client: ClienteModel,
        con_rd,
        robot: str,
        queue
    ) -> None:
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.client = client
        self.con_rd = con_rd
        self.robot = robot
        self.queue = queue

    def execute(self) -> Union[DadosEntradaEspaiderModel, DadosEntradaEspaiderExpModel]:
        message = "Iniciando validação dos campos de entrada"
        self.classLogger.message(message)
        if self.robot != 'Expediente':
            ValidarDadosEntradaUseCase(
                classLogger=self.classLogger,
                json_recebido=self.json_recebido
            ).execute(type_robot=self.robot)
            return FormatarDadosEntradaUseCase(
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                client=self.client,
                con_rd=self.con_rd,
                robot=self.robot,
                queue=self.queue
            ).execute()
        else:
            ValidarDadosEntradaExpUseCase
            return FormatarDadosEntradaExpUseCase(
                classLogger=self.classLogger,
                json_recebido=self.json_recebido,
                client=self.client,
                con_rd=self.con_rd,
                robot=self.robot,
                queue=self.queue
            ).execute()
