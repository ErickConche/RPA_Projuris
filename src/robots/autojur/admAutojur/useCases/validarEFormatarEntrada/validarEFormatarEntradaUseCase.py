
import json
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from modules.formatacao.formatacao import Formatacao
from models.cookies.cookiesUseCase import CookiesUseCase
from robots.autojur.admAutojur.useCases.correcaoErrosUsuario.correcaoErrosUsuarioUseCase import CorrecaoErrosUsuarioUseCase
from robots.autojur.admAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


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

        if not fields.get("Reclamacao") or fields.get("Reclamacao") is None:
            raise Exception("Informe a reclamação")
        
        if not fields.get("Pasta") or fields.get("Pasta") is None:
            raise Exception("Informe a pasta")
        
        if not fields.get("DataSolicitacao") or fields.get("DataSolicitacao") is None:
            raise Exception("Informe a data da solicitação")
        
        if not fields.get("UF") or fields.get("UF") is None:
            raise Exception("Informe a UF")
        
        if not fields.get("Cidade") or fields.get("Cidade") is None:
            raise Exception("Informe a cidade")
        
        if not fields.get("NomeEmpresa") or fields.get("NomeEmpresa") is None:
            raise Exception("Informe o nome da empresa")
        
        if not fields.get("NomeEnvolvido") or fields.get("NomeEnvolvido") is None:
            raise Exception("Informe o nome do envolvido")
        
        if not fields.get("CpfCnpjEnvolvido") or fields.get("CpfCnpjEnvolvido") is None:
            raise Exception("Informe o cpf ou cnpj do envolvido")
        
        if len(fields.get("CpfCnpjEnvolvido"))!=14 and len(fields.get("CpfCnpjEnvolvido"))!=11:
            raise Exception("CPF invalido")
        
        if not fields.get("Sistema") or fields.get("Sistema") is None:
            raise Exception("Informe o tipo do sistema")
        
        if not fields.get("NomeProcon") or fields.get("NomeProcon") is None:
            raise Exception("Informe o nome do Procon")
        
        if not fields.get("DadosReserva") or fields.get("DadosReserva") is None:
            raise Exception("Informe os dados reserva")
        
        if not fields.get("ArquivoPrincipal") or fields.get("ArquivoPrincipal") is None:
            raise Exception("Informe a url do arquivo principal")
        
        if not fields.get("Observacao") or fields.get("Observacao") is None:
            raise Exception("Informe as observações")

        # Obtenha a hora atual no fuso horário do Brasil
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
        
        data_input: DadosEntradaFormatadosModel = DadosEntradaFormatadosModel(
            username=usuario,
            password=senha,
            footprint=cookie.conteudo,
            url_cookie=cookie.url,
            numero_reclamacao=fields.get("Reclamacao"),
            pasta=fields.get("Pasta"),
            data_solicitacao=Formatacao().formatarData(fields.get("DataSolicitacao")),
            uf=fields.get("UF").replace("-"," "),
            cidade=fields.get("Cidade").strip(),
            tipo_processo=fields.get("TipoProcesso") if fields.get("TipoProcesso") and fields.get("TipoProcesso") is not None else 'Reclamação',
            tipo_extrajudicial=fields.get("TipoExtrajudicial").replace("-"," ") if fields.get("TipoExtrajudicial") and fields.get("TipoExtrajudicial") is not None else 'Contencioso Administrativo',
            empresa='BOOKING.COM BRASIL SERVIÇOS DE RESERVA DE HOTÉIS LTDA',
            situacao=fields.get("Situacao") if fields.get("Situacao") and fields.get("Situacao") is not None else 'Ativo',
            qualificacao_empresa='CLIENTE - CLIENTE',
            nome_envolvido=fields.get("NomeEnvolvido"),
            cpf_cnpj_envolvido=Formatacao().formatarCpfCnpj(fields.get("CpfCnpjEnvolvido")),
            tipo_envolvido=fields.get("TipoEnvolvido") if fields.get("TipoEnvolvido") and fields.get("TipoEnvolvido") is not None else 'Fisico',
            qualificacao_envolvido='PARTE ADVERSA - PARTE_CONTRARIA',
            tipo_sistema=fields.get("Sistema"),
            qualificacao_sistema='NOTIFICANTE',
            nome_procon=fields.get("NomeProcon"),
            tipo_reclamacao=fields.get("TipoReclamacao") if fields.get("TipoReclamacao") and fields.get("TipoReclamacao") is not None else 'Digital',
            dados_reserva=fields.get("DadosReserva"),
            arquivo_principal=fields.get("ArquivoPrincipal"),
            observacoes=fields.get("Observacao")
        )

        data_input = CorrecaoErrosUsuarioUseCase(data_input=data_input).execute()
        
        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)

        return data_input