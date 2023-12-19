
import json
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
        if not fields.get("Sistema") or not Deparas.depara_sistema(fields.get("Sistema")):
            raise Exception("Informe o tipo do sistema")

        if not fields.get("PosicaoEnvolvido") or not Deparas.depara_posicao_reclamante(fields.get("PosicaoEnvolvido")):
            raise Exception("Informe a posição do envolvido")
        
        if not fields.get("TipoReclamacao") or not Deparas.depara_tipo_reclamacao(fields.get("TipoReclamacao")):
            raise Exception("Informe o tipo da reclamação")
        
        if not fields.get("TipoProcesso") or not Deparas.depara_tipo_processo(fields.get("TipoProcesso")):
            raise Exception("Informe o tipo do processo")
        
        ##Demais infos
        if not fields.get("UF"):
            raise Exception("Informe a UF")
        
        if not fields.get("Cidade"):
            raise Exception("Informe a cidade")
        
        if not fields.get("DataSolicitacao"):
            raise Exception("Informe a data de solicitação")
        
        if not fields.get("NomeEmpresa"):
            raise Exception("Informe o nome da empresa")
        
        if not fields.get("NomeEnvolvido"):
            raise Exception("Informe o nome do envolvido")
        
        if not fields.get("CpfCnpjEnvolvido"):
            raise Exception("Informe o cpf ou cnpj do envolvido")
        
        if not fields.get("TipoEnvolvido"):
            raise Exception("Informe o tipo do envolvido")
        
        if not fields.get("Observacao"):
            raise Exception("Informe a observação")
        
        if not fields.get("NomeProcon"):
            raise Exception("Informe o nome do Procon")
        
        if not fields.get("Reclamacao"):
            raise Exception("Informe o numero da reclamação")
        
        if not fields.get("DadosReserva"):
            raise Exception("Informe os dados reserva")
        
        if not fields.get("ArquivoPrincipal"):
            raise Exception("Informe a url do arquivo principal")
        
        if not fields.get("ArquivosSecundarios"):
            raise Exception("Informe as urls dos arquivos secundarios")
        
        data_input: DadosEntradaFormatadosModel = DadosEntradaFormatadosModel(
            username="ConsumidorBaz",
            password="@BazConsumidor",
            tipo_sistema=fields.get("Sistema"),
            uf=fields.get("UF"),
            cidade=fields.get("Cidade"),
            data_solicitacao=fields.get("DataSolicitacao"),
            empresa=fields.get("NomeEmpresa"),
            posicao_envolvido=fields.get("PosicaoEnvolvido"),
            nome_envolvido=fields.get("NomeEnvolvido"),
            cpf_cnpj_envolvido=fields.get("CpfCnpjEnvolvido"),
            tipo_envolvido=fields.get("TipoEnvolvido"),
            observacoes=fields.get("Observacao"),
            id_acomodacao=fields.get("IdAcomodacao") if fields.get("IdAcomodacao") else '0000',
            numero_reserva=fields.get("NumeroReserva") if fields.get("NumeroReserva") else '0000',
            nome_procon=fields.get("NomeProcon"),
            numero_reclamacao=fields.get("Reclamacao"),
            tipo_reclamacao=fields.get("TipoReclamacao"),
            tipo_processo=fields.get("TipoProcesso"),
            dados_reserva=fields.get("DadosReserva"),
            arquivo_principal=fields.get("ArquivoPrincipal"),
            arquivos_secundarios=fields.get("ArquivosSecundarios")
        )
        
        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)

        return data_input