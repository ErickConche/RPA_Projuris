
import json
import pytz
from datetime import datetime
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from robots.admLegalone.useCases.deparas.deparas import Deparas
from robots.admLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


class ValidarEFormatarEntradaUseCase:
    def __init__(
        self,
        classLogger: Logger,
        json_recebido:str,
        cliente:Cliente
    ) -> None:
        self.classLogger = classLogger
        self.json_recebido = json_recebido
        self.cliente = cliente

    def execute(self)-> DadosEntradaFormatadosModel:
        message = "Iniciando validação dos campos de entrada"
        self.classLogger.message(message)
        json_recebido:dict = json.loads(self.json_recebido)
        fields:dict = json_recebido.get("Fields")
        
        ##Deparas
        if not fields.get("Sistema") or not Deparas.depara_sistema(fields.get("Sistema")) or fields.get("Sistema") is None:
            raise Exception("Informe o tipo do sistema")
    
        
        if not fields.get("TipoProcesso") or not Deparas.depara_tipo_processo(fields.get("TipoProcesso")) or fields.get("TipoProcesso") is None:
            raise Exception("Informe o tipo do processo")
        
        ##Demais infos
        if not fields.get("UF") or fields.get("UF") is None:
            raise Exception("Informe a UF")
        
        if not fields.get("Cidade") or fields.get("Cidade") is None:
            raise Exception("Informe a cidade")
        
        if not fields.get("DataSolicitacao") or fields.get("DataSolicitacao") is None:
            raise Exception("Informe a data de solicitação")
        
        if not fields.get("NomeEmpresa") or fields.get("NomeEmpresa") is None:
            raise Exception("Informe o nome da empresa")
        
        if not fields.get("NomeEnvolvido") or fields.get("NomeEnvolvido") is None:
            raise Exception("Informe o nome do envolvido")
        
        if not fields.get("CpfCnpjEnvolvido") or fields.get("CpfCnpjEnvolvido") is None:
            raise Exception("Informe o cpf ou cnpj do envolvido")
        
        if not fields.get("TipoEnvolvido") or fields.get("TipoEnvolvido") is None:
            raise Exception("Informe o tipo do envolvido")
        
        if not fields.get("Observacao") or fields.get("Observacao") is None:
            raise Exception("Informe a observação")
        
        if not fields.get("NomeProcon") or fields.get("NomeProcon") is None:
            raise Exception("Informe o nome do Procon")
        
        if not fields.get("Reclamacao") or fields.get("Reclamacao") is None:
            raise Exception("Informe o numero da reclamação")
        
        if not fields.get("DadosReserva") or fields.get("DadosReserva") is None:
            raise Exception("Informe os dados reserva")
        
        if not fields.get("ArquivoPrincipal") or fields.get("ArquivoPrincipal") is None:
            raise Exception("Informe a url do arquivo principal")
        
        if not fields.get("ArquivosSecundarios") or fields.get("ArquivosSecundarios") is None:
            raise Exception("Informe as urls dos arquivos secundarios")
        
        fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')

        # Obtenha a hora atual no fuso horário do Brasil
        hora_atual_brasil = datetime.now(fuso_horario_brasil).hour
        usuario = ""
        senha = ""
        if  hora_atual_brasil < 12:
            usuario = "ConsumidorBaz"
            senha = "@BazConsumidor"
        
        else:
            usuario = "BazLegalOne"
            senha = "@Baz1978"

        
        data_input: DadosEntradaFormatadosModel = DadosEntradaFormatadosModel(
            username=usuario,
            password=senha,
            tipo_sistema=fields.get("Sistema"),
            uf=fields.get("UF"),
            cidade=fields.get("Cidade"),
            data_solicitacao=fields.get("DataSolicitacao"),
            empresa=fields.get("NomeEmpresa"),
            posicao_envolvido=fields.get("PosicaoEnvolvido") if fields.get("PosicaoEnvolvido") and fields.get("PosicaoEnvolvido") is not None else 'Reclamante',
            nome_envolvido=fields.get("NomeEnvolvido"),
            cpf_cnpj_envolvido=fields.get("CpfCnpjEnvolvido"),
            tipo_envolvido=fields.get("TipoEnvolvido"),
            observacoes=fields.get("Observacao"),
            id_acomodacao=fields.get("IdAcomodacao") if fields.get("IdAcomodacao") and fields.get("IdAcomodacao") is not None else '0000',
            numero_reserva=fields.get("NumeroReserva") if fields.get("NumeroReserva") and fields.get("NumeroReserva") is not None else '0000',
            nome_procon=fields.get("NomeProcon"),
            numero_reclamacao=fields.get("Reclamacao"),
            tipo_reclamacao=fields.get("TipoReclamacao") if fields.get("TipoReclamacao") and fields.get("TipoReclamacao") is not None else 'Digital',
            tipo_processo=fields.get("TipoProcesso"),
            dados_reserva=fields.get("DadosReserva"),
            arquivo_principal=fields.get("ArquivoPrincipal"),
            arquivos_secundarios=fields.get("ArquivosSecundarios")
        )
        
        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)

        return data_input