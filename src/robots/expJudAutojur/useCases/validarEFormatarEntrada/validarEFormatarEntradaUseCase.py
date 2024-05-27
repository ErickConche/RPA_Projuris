
import json
from models.cookies.cookiesUseCase import CookiesUseCase
from modules.formatacao.formatacao import Formatacao
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from modules.validacao.validacao import Validacao
from robots.expJudAutojur.useCases.correcaoErrosUsuario.correcaoErrosUsuarioUseCase import CorrecaoErrosUsuarioUseCase
from robots.expJudAutojur.useCases.deparas.deparas import Deparas
from robots.expJudAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class ValidarEFormatarEntradaUseCase:
    def __init__(
        self,
        classLogger: Logger,
        json_recebido:str,
        cliente:Cliente,
        queue: str,
        con_rd,
    ) -> None:
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.cliente = cliente
        self.con_rd = con_rd
        self.queue = queue
        self.depara = Deparas()
        self.formatacao = Formatacao()
        self.validacao = Validacao()

    def execute(self)-> DadosEntradaFormatadosModel:
        message = "Iniciando validação dos campos de entrada"
        self.classLogger.message(message)
        fields:dict = self.json_recebido.get("Fields")

        if not fields.get("Processo") or fields.get("Processo") is None:
            raise Exception("Informe o número do processo")
        
        if not fields.get("Evento") or fields.get("Evento") is None:
            raise Exception("Informe o evento")
        
        evento = fields.get("Evento").strip()
        if self.depara.depara_evento(evento) is None:
            raise Exception("O Evento informado não foi mapeado")
        
        if not fields.get("DataExpediente") or fields.get("DataExpediente") is None:
            raise Exception("Informe a data")
        
        if not fields.get("HoraExpediente") and fields.get("HoraExpediente") is None:
            raise Exception("A hora informada é invalida")
        
        if not fields.get("Responsavel") or fields.get("Responsavel") is None:
            raise Exception("Informe o responsavel")
        
        arquivo = fields.get("Files") or '.'

        arquivo = self.formatacao.formatarArquivo(arquivo)

        # Obtenha a hora atual no fuso horário do Brasil
        usuario = "docato3"
        senha = "Docatoexpedientes3"

        message = (f"Usando o usuário {usuario} para login")
        self.classLogger.message(message)

        cookie = CookiesUseCase(con_rd=self.con_rd).buscarCookies(
            idcliente=self.cliente.id,
            queue=self.queue
        )

        if not cookie:
            raise Exception("O sessão está expirada, favor entrar em contato do equipe de desenvolvimento para renovar sessão")
        
        data = self.formatacao.formatarData(fields.get("DataExpediente").strip())
        hora = fields.get("HoraExpediente").strip() or '00:00'
        if len(hora.split(":")) > 2:
            hora_split = hora.split(":")
            hora = hora_split[0] + ":" + hora_split[1]

        if not self.validacao.validar_hora(hora):
            raise Exception("O formato da hora está incorreto")
        
        data_formatada = f"{data} {hora}" \
            if self.depara.depara_usa_data_hora_evento(evento) is not None \
          else data

        data_input: DadosEntradaFormatadosModel = DadosEntradaFormatadosModel(
            username=usuario,
            password=senha,
            footprint=cookie.conteudo,
            url_cookie=cookie.url,
            cookie_session=cookie.session_cookie,
            processo=fields.get("Processo").strip(),
            evento=fields.get("Evento").strip(),
            id_evento=self.depara.depara_evento(evento),
            tipo_evento='Judicial', 
            data=data_formatada,
            data_final=data,
            responsavel=fields.get("Responsavel").strip(),
            arquivo=arquivo
        )

        data_input = CorrecaoErrosUsuarioUseCase(data_input=data_input).execute()

        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)

        return data_input
    