
import json
import pytz
from datetime import datetime
from modules.formatacao.formatacao import Formatacao
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
    
        
        fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')

        # Obtenha a hora atual no fuso horário do Brasil
        hora_atual_brasil = datetime.now(fuso_horario_brasil).hour
        usuario = ""
        senha = ""
        if  hora_atual_brasil < 12:
            usuario = "ConsumidorBaz"
            senha = "@BazConsumidor"
        
        else:
            usuario = "ConsumidorBaz"
            senha = "@BazConsumidor"

        message = (f"Usando o usuário {usuario} para login")
        self.classLogger.message(message)
        
        data_input: DadosEntradaFormatadosModel = DadosEntradaFormatadosModel(
            username=usuario,
            password=senha,
            tipo_sistema=fields.get("Sistema"),
            uf=fields.get("UF").replace("-"," "),
            cidade=fields.get("Cidade"),
            data_solicitacao=Formatacao().formatarData(fields.get("DataSolicitacao")),
            empresa='BOOKING.COM BRASIL SERVIÇOS DE RESERVA DE HOTÉIS LTDA',
            posicao_envolvido=fields.get("PosicaoEnvolvido") if fields.get("PosicaoEnvolvido") and fields.get("PosicaoEnvolvido") is not None else 'Reclamante',
            nome_envolvido=fields.get("NomeEnvolvido"),
            cpf_cnpj_envolvido=Formatacao().formatarCpfCnpj(fields.get("CpfCnpjEnvolvido")),
            tipo_envolvido=fields.get("TipoEnvolvido") if fields.get("TipoEnvolvido") and fields.get("TipoEnvolvido") is not None else 'Fisico',
            observacoes=fields.get("Observacao"),
            id_acomodacao=fields.get("IdAcomodacao") if fields.get("IdAcomodacao") and fields.get("IdAcomodacao") is not None else '0000',
            numero_reserva=fields.get("NumeroReserva") if fields.get("NumeroReserva") and fields.get("NumeroReserva") is not None else '0000',
            nome_procon=fields.get("NomeProcon"),
            numero_reclamacao=fields.get("Reclamacao"),
            tipo_reclamacao=fields.get("TipoReclamacao") if fields.get("TipoReclamacao") and fields.get("TipoReclamacao") is not None else 'Digital',
            tipo_processo=fields.get("TipoProcesso"),
            dados_reserva=fields.get("DadosReserva"),
            arquivo_principal=fields.get("ArquivoPrincipal"),
            arquivos_secundarios=fields.get("ArquivosSecundarios") if fields.get("ArquivosSecundarios") and fields.get("ArquivosSecundarios") is not None else 'Nenhum arquivo anexado'
        )
        

        if data_input.tipo_processo == 'C.I.P':
            data_input.tipo_processo = 'C.I.P.'
        
        if data_input.tipo_sistema == 'PROCON-Consumidorgovbr':
            data_input.tipo_sistema = "PROCON / Consumidor.gov.br"

        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)

        if len(data_input.data_solicitacao.split("/")[-1]) == 2:
            dia, mes, ano = data_input.data_solicitacao.split('/')
            if len(ano):
                ano = '20' + ano
            data_input.data_solicitacao =  f'{dia}/{mes}/{ano}'

        return data_input