
import json
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from models.cookies.cookiesUseCase import CookiesUseCase
from robots.autojur.identCadastroAutojur.useCases.validarEFormatarEntrada.__model__.dadosEntradaFormatadosModel import DadosEntradaFormatadosModel


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
        self.is_adm = False

    def execute(self)-> DadosEntradaFormatadosModel:
        message = "Iniciando validação dos campos de entrada"
        self.classLogger.message(message)
        json_recebido:dict = json.loads(self.json_recebido)
        fields:dict = json_recebido.get("Fields")

        if not fields.get("Processo") or fields.get("Processo") is None:
            result = self.check_adm(fields)
            if not result:
                raise Exception("Informe os campos para fazer a busca de um processo.")
        
        usuario = "docato3"
        senha = "Docatoexpedientes3"

        message = (f"Usando o usuário {usuario} para login")
        self.classLogger.message(message)

        cookie = CookiesUseCase(
            con_rd=self.con_rd
        ).buscarCookies(
            queue="app-identificar-cadastro-autojur",
            idcliente=self.cliente.id
        )

        if not cookie:
            raise Exception("O sessão está expirada, favor entrar em contato do equipe de desenvolvimento para renovar sessão")
        
        if self.is_adm:
                data_input: DadosEntradaFormatadosModel= DadosEntradaFormatadosModel(
                username=usuario,
                password=senha,
                footprint=cookie.conteudo,
                url_cookie=cookie.url,
                processo='',
                reclamacao=fields.get("Protocolo").strip(),
                pessoa=fields.get("NomeParte").strip()
            )
        else:
            data_input: DadosEntradaFormatadosModel = DadosEntradaFormatadosModel(
                username=usuario,
                password=senha,
                footprint=cookie.conteudo,
                url_cookie=cookie.url,
                processo=fields.get("Processo").strip(),
                reclamacao='',
                pessoa='',
            )

        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)

        return data_input
    
    def check_adm(self, fields):
        try:
            if not fields.get("Protocolo") or fields.get("Protocolo") is None:
                raise Exception ("Informe o número do protocolo/reclamação/número do processo administrativo.")
            if not fields.get("NomeParte") or fields.get("NomeParte") is None:
                raise Exception ("Informe o nome da parte contrária.")

            self.is_adm = True
            return True
        except Exception:
            raise Exception("Informe o número do processo judicial.")