
import json
import pytz
from datetime import datetime
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from robots.judLegalone.useCases.deparas.deparas import Deparas
from robots.judLegalone.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


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

        if not fields.get("Titulo") or fields.get("Titulo") is None:
            raise Exception("Informe a Titulo")

        if not fields.get("Processo") or fields.get("Processo") is None:
            raise Exception("Informe o número do processo")
        
        if not fields.get("DataDistribuicao") or fields.get("DataDistribuicao") is None:
            raise Exception("Informe a data de distribuicao")
        
        if not fields.get("Procedimento") or fields.get("Procedimento") is None:
            raise Exception("Informe o procedimento")

        if not fields.get("UF") or fields.get("UF") is None:
            raise Exception("Informe a UF")
        
        if not fields.get("Cidade") or fields.get("Cidade") is None:
            raise Exception("Informe a cidade")
        
        if not fields.get("OrgaoJulgador") or fields.get("OrgaoJulgador") is None:
            raise Exception("Informe o orgão")
        
        if not fields.get("Comarca") or fields.get("Comarca") is None:
            raise Exception("Informe a comarca")
        
        if not fields.get("ComplementoComarca") or fields.get("ComplementoComarca") is None:
            raise Exception("Informe o complemento da comarca")
        
        if not fields.get("NumeroVara") or fields.get("NumeroVara") is None:
            raise Exception("Informe o número da vara")
        
        if not fields.get("Vara") or fields.get("Vara") is None:
            raise Exception("Informe a vara")

        if not fields.get("NomeEnvolvido") or fields.get("NomeEnvolvido") is None:
            raise Exception("Informe o nome do envolvido")
        
        if not fields.get("CpfCnpjEnvolvido") or fields.get("CpfCnpjEnvolvido") is None:
            raise Exception("Informe o cpf ou cnpj do envolvido")
        
        if not fields.get("ArquivoPrincipal") or fields.get("ArquivoPrincipal") is None:
            raise Exception("Informe a url do arquivo principal")
        
        usuario = "BazLegalOne"
        senha = "@Baz1978"

        message = (f"Usando o usuário {usuario} para login")
        self.classLogger.message(message)
        
        data_input: DadosEntradaFormatadosModel = DadosEntradaFormatadosModel(
            username=usuario,
            password=senha,
            processo_originario=fields.get("ProcessoOriginario") if fields.get("ProcessoOriginario") and fields.get("ProcessoOriginario") is not None else '',
            justica=fields.get("Justica") if fields.get("Justica") and fields.get("Justica") is not None else 'Justiça Estadual',
            titulo=fields.get("Titulo"),
            processo=fields.get("Processo"),
            data_distribuicao=fields.get("DataDistribuicao"),
            procedimento=fields.get("Procedimento"),
            uf=fields.get("UF"),
            cidade=fields.get("Cidade"),
            orgao_julgador=fields.get("OrgaoJulgador"),
            natureza=fields.get("Natureza") if fields.get("Natureza") and fields.get("Natureza") is not None else 'Cível',
            fase=fields.get("Fase") if fields.get("Fase") and fields.get("Fase") is not None else 'Inicial',
            comarca=fields.get("Comarca"),
            complemento_comarca=fields.get("ComplementoComarca"),
            numero_vara=fields.get("NumeroVara"),
            complemento_vara=fields.get("ComplementoVara") if fields.get("ComplementoVara") and fields.get("ComplementoVara") is not None else 'Não',
            vara=fields.get("Vara"),
            empresa=fields.get("NomeEmpresa") if fields.get("NomeEmpresa") and fields.get("NomeEmpresa") is not None else 'Booking.com Brasil Serviços de Reserva de Hotéis Ltda',
            nome_envolvido=fields.get("NomeEnvolvido"),
            cpf_cnpj_envolvido=fields.get("CpfCnpjEnvolvido"),
            situacao_outros_envolvidos1=fields.get("SituacaoOutrosEnvolvidos1") if fields.get("SituacaoOutrosEnvolvidos1") and fields.get("SituacaoOutrosEnvolvidos1") is not None else 'Parte',
            posicao_outros_envolvidos1=fields.get("PosicaoOutrosEnvolvidos1") if fields.get("PosicaoOutrosEnvolvidos1") and fields.get("PosicaoOutrosEnvolvidos1") is not None else '',
            nome_outros_envolvidos1=fields.get("NomeOutrosEnvolvidos1") if fields.get("NomeOutrosEnvolvidos1") and fields.get("NomeOutrosEnvolvidos1") is not None else '',
            cpf_cnpj_outros_envolvidos1=fields.get("CpfCnpjOutrosEnvolvidos1") if fields.get("CpfCnpjOutrosEnvolvidos1") and fields.get("CpfCnpjOutrosEnvolvidos1") is not None else '',
            situacao_outros_envolvidos2=fields.get("SituacaoOutrosEnvolvidos2") if fields.get("SituacaoOutrosEnvolvidos2") and fields.get("SituacaoOutrosEnvolvidos2") is not None else 'Parte',
            posicao_outros_envolvidos2=fields.get("PosicaoOutrosEnvolvidos2") if fields.get("PosicaoOutrosEnvolvidos2") and fields.get("PosicaoOutrosEnvolvidos2") is not None else '',
            nome_outros_envolvidos2=fields.get("NomeOutrosEnvolvidos2") if fields.get("NomeOutrosEnvolvidos2") and fields.get("NomeOutrosEnvolvidos2") is not None else '',
            cpf_cnpj_outros_envolvidos2=fields.get("CpfCnpjOutrosEnvolvidos2") if fields.get("CpfCnpjOutrosEnvolvidos2") and fields.get("CpfCnpjOutrosEnvolvidos2") is not None else '',
            situacao_outros_envolvidos3=fields.get("SituacaoOutrosEnvolvidos3") if fields.get("SituacaoOutrosEnvolvidos3") and fields.get("SituacaoOutrosEnvolvidos3") is not None else 'Parte',
            posicao_outros_envolvidos3=fields.get("PosicaoOutrosEnvolvidos3") if fields.get("PosicaoOutrosEnvolvidos3") and fields.get("PosicaoOutrosEnvolvidos3") is not None else '',
            nome_outros_envolvidos3=fields.get("NomeOutrosEnvolvidos3") if fields.get("NomeOutrosEnvolvidos3") and fields.get("NomeOutrosEnvolvidos3") is not None else '',
            cpf_cnpj_outros_envolvidos3=fields.get("CpfCnpjOutrosEnvolvidos3") if fields.get("CpfCnpjOutrosEnvolvidos3") and fields.get("CpfCnpjOutrosEnvolvidos3") is not None else '',
            situacao_outros_envolvidos4=fields.get("SituacaoOutrosEnvolvidos4") if fields.get("SituacaoOutrosEnvolvidos4") and fields.get("SituacaoOutrosEnvolvidos4") is not None else 'Parte',
            posicao_outros_envolvidos4=fields.get("PosicaoOutrosEnvolvidos4") if fields.get("PosicaoOutrosEnvolvidos4") and fields.get("PosicaoOutrosEnvolvidos4") is not None else '',
            nome_outros_envolvidos4=fields.get("NomeOutrosEnvolvidos4") if fields.get("NomeOutrosEnvolvidos4") and fields.get("NomeOutrosEnvolvidos4") is not None else '',
            cpf_cnpj_outros_envolvidos4=fields.get("CpfCnpjOutrosEnvolvidos4") if fields.get("CpfCnpjOutrosEnvolvidos4") and fields.get("CpfCnpjOutrosEnvolvidos4") is not None else '',
            situacao_outros_envolvidos5=fields.get("SituacaoOutrosEnvolvidos5") if fields.get("SituacaoOutrosEnvolvidos5") and fields.get("SituacaoOutrosEnvolvidos5") is not None else 'Parte',
            posicao_outros_envolvidos5=fields.get("PosicaoOutrosEnvolvidos5") if fields.get("PosicaoOutrosEnvolvidos5") and fields.get("PosicaoOutrosEnvolvidos5") is not None else '',
            nome_outros_envolvidos5=fields.get("NomeOutrosEnvolvidos5") if fields.get("NomeOutrosEnvolvidos5") and fields.get("NomeOutrosEnvolvidos5") is not None else '',
            cpf_cnpj_outros_envolvidos5=fields.get("CpfCnpjOutrosEnvolvidos5") if fields.get("CpfCnpjOutrosEnvolvidos5") and fields.get("CpfCnpjOutrosEnvolvidos5") is not None else '',
            situacao_outros_envolvidos6=fields.get("SituacaoOutrosEnvolvidos6") if fields.get("SituacaoOutrosEnvolvidos6") and fields.get("SituacaoOutrosEnvolvidos6") is not None else 'Parte',
            posicao_outros_envolvidos6=fields.get("PosicaoOutrosEnvolvidos6") if fields.get("PosicaoOutrosEnvolvidos6") and fields.get("PosicaoOutrosEnvolvidos6") is not None else '',
            nome_outros_envolvidos6=fields.get("NomeOutrosEnvolvidos6") if fields.get("NomeOutrosEnvolvidos6") and fields.get("NomeOutrosEnvolvidos6") is not None else '',
            cpf_cnpj_outros_envolvidos6=fields.get("CpfCnpjOutrosEnvolvidos6") if fields.get("CpfCnpjOutrosEnvolvidos6") and fields.get("CpfCnpjOutrosEnvolvidos6") is not None else '',
            situacao_outros_envolvidos7=fields.get("SituacaoOutrosEnvolvidos7") if fields.get("SituacaoOutrosEnvolvidos7") and fields.get("SituacaoOutrosEnvolvidos7") is not None else 'Parte',
            posicao_outros_envolvidos7=fields.get("PosicaoOutrosEnvolvidos7") if fields.get("PosicaoOutrosEnvolvidos7") and fields.get("PosicaoOutrosEnvolvidos7") is not None else '',
            nome_outros_envolvidos7=fields.get("NomeOutrosEnvolvidos7") if fields.get("NomeOutrosEnvolvidos7") and fields.get("NomeOutrosEnvolvidos7") is not None else '',
            cpf_cnpj_outros_envolvidos7=fields.get("CpfCnpjOutrosEnvolvidos7") if fields.get("CpfCnpjOutrosEnvolvidos7") and fields.get("CpfCnpjOutrosEnvolvidos7") is not None else '',
            situacao_outros_envolvidos8=fields.get("SituacaoOutrosEnvolvidos8") if fields.get("SituacaoOutrosEnvolvidos8") and fields.get("SituacaoOutrosEnvolvidos8") is not None else 'Parte',
            posicao_outros_envolvidos8=fields.get("PosicaoOutrosEnvolvidos8") if fields.get("PosicaoOutrosEnvolvidos8") and fields.get("PosicaoOutrosEnvolvidos8") is not None else '',
            nome_outros_envolvidos8=fields.get("NomeOutrosEnvolvidos8") if fields.get("NomeOutrosEnvolvidos8") and fields.get("NomeOutrosEnvolvidos8") is not None else '',
            cpf_cnpj_outros_envolvidos8=fields.get("CpfCnpjOutrosEnvolvidos8") if fields.get("CpfCnpjOutrosEnvolvidos8") and fields.get("CpfCnpjOutrosEnvolvidos8") is not None else '',
            situacao_outros_envolvidos9=fields.get("SituacaoOutrosEnvolvidos9") if fields.get("SituacaoOutrosEnvolvidos9") and fields.get("SituacaoOutrosEnvolvidos9") is not None else 'Parte',
            posicao_outros_envolvidos9=fields.get("PosicaoOutrosEnvolvidos9") if fields.get("PosicaoOutrosEnvolvidos9") and fields.get("PosicaoOutrosEnvolvidos9") is not None else '',
            nome_outros_envolvidos9=fields.get("NomeOutrosEnvolvidos9") if fields.get("NomeOutrosEnvolvidos9") and fields.get("NomeOutrosEnvolvidos9") is not None else '',
            cpf_cnpj_outros_envolvidos9=fields.get("CpfCnpjOutrosEnvolvidos9") if fields.get("CpfCnpjOutrosEnvolvidos9") and fields.get("CpfCnpjOutrosEnvolvidos9") is not None else '',
            situacao_outros_envolvidos10=fields.get("SituacaoOutrosEnvolvidos10") if fields.get("SituacaoOutrosEnvolvidos10") and fields.get("SituacaoOutrosEnvolvidos10") is not None else 'Parte',
            posicao_outros_envolvidos10=fields.get("PosicaoOutrosEnvolvidos10") if fields.get("PosicaoOutrosEnvolvidos10") and fields.get("PosicaoOutrosEnvolvidos10") is not None else '',
            nome_outros_envolvidos10=fields.get("NomeOutrosEnvolvidos10") if fields.get("NomeOutrosEnvolvidos10") and fields.get("NomeOutrosEnvolvidos10") is not None else '',
            cpf_cnpj_outros_envolvidos10=fields.get("CpfCnpjOutrosEnvolvidos10") if fields.get("CpfCnpjOutrosEnvolvidos10") and fields.get("CpfCnpjOutrosEnvolvidos10") is not None else '',
            id_acomodacao=fields.get("IdAcomodacao") if fields.get("IdAcomodacao") and fields.get("IdAcomodacao") is not None else '0000',
            numero_reserva=fields.get("NumeroReserva") if fields.get("NumeroReserva") and fields.get("NumeroReserva") is not None else '0000',
            data_citacao=fields.get("DataCitacao") if fields.get("DataCitacao") and fields.get("DataCitacao") is not None else '',
            arquivo_principal=fields.get("ArquivoPrincipal")
        )

        if data_input.complemento_comarca == 'Capital Copacabana':
            data_input.complemento_comarca = 'Copacabana'

        if data_input.complemento_comarca == '2° JD':
            data_input.complemento_comarca = '2ª JD'

        if data_input.complemento_comarca == '29° JD':
            data_input.complemento_comarca = '29º JD da Comarca de Belo Horizonte'

        if data_input.comarca == 'Norte da Ilha':
            data_input.comarca = 'Norte Da Ilha'

        if data_input.comarca == 'Embu das Artes':
            data_input.comarca = 'Embu Das Artes'

            

        if data_input.vara == 'Vara do Juizado Especial Cível':
            data_input.vara = 'Vara Do Juizado Especial Cível'

        elif data_input.vara == 'Vara do Juizado Especial Central':
            data_input.vara = 'Vara Do Juizado Especial Central'

        elif data_input.vara == 'Vara Juizado Especial Cível e Criminal':
            data_input.vara = 'Do Juizado Especial Cível E Criminal'


            

        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)

        return data_input