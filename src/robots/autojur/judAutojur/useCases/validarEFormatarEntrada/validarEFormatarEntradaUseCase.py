
import json
from modules.logger.Logger import Logger
from models.cliente.cliente import Cliente
from models.cookies.cookiesUseCase import CookiesUseCase
from robots.autojur.judAutojur.useCases.correcaoErrosUsuario.correcaoErrosUsuarioUseCase import CorrecaoErrosUsuarioUseCase
from robots.autojur.judAutojur.useCases.validarEFormatarEntrada.__model__.DadosEntradaFormatadosModel import DadosEntradaFormatadosModel


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
        
        if not fields.get("Pasta") or fields.get("Pasta") is None:
            raise Exception("Informe a pasta")
        
        pasta = fields.get("Pasta")

        if 'Pasta n' not in fields.get("Pasta"):
            pasta = f"Pasta nº {pasta}"
        
        if not fields.get("Titulo") or fields.get("Titulo") is None:
            raise Exception("Informe o Titulo/Tipo de ação")
        
        if not fields.get("DataDistribuicao") or fields.get("DataDistribuicao") is None:
            raise Exception("Informe a data de distribuição")
        
        if not fields.get("UF") or fields.get("UF") is None:
            raise Exception("Informe a UF")
        
        if not fields.get("Cidade") or fields.get("Cidade") is None:
            raise Exception("Informe a cidade")
        
        if not fields.get("OrgaoJulgador") or fields.get("OrgaoJulgador") is None:
            raise Exception("Informe o orgão julgador")
        
        if not fields.get("Rito") or fields.get("Rito") is None:
            raise Exception("Informe o rito")
        
        if not fields.get("CpfCnpjEnvolvido") or fields.get("CpfCnpjEnvolvido") is None:
            raise Exception("Informe o cpf ou cnpj do envolvido")
        
        if not fields.get("NomeEnvolvido") or fields.get("NomeEnvolvido") is None:
            raise Exception("Informe o nome do envolvido")
        
        if not fields.get("SistemaTribunal") or fields.get("SistemaTribunal") is None:
            raise Exception("Informe o sistema")
        
        if not fields.get("ArquivoPrincipal") or fields.get("ArquivoPrincipal") is None:
            raise Exception("Informe a url do arquivo principal")

        # Obtenha a hora atual no fuso horário do Brasil
        usuario = "docato2"
        senha = "Docatojudicial2"

        message = (f"Usando o usuário {usuario} para login")
        self.classLogger.message(message)

        cookie = CookiesUseCase(
            con_rd=self.con_rd
        ).buscarCookies(
            queue="app-jud-autojur",
            idcliente=self.cliente.id
        )

        if not cookie:
            raise Exception("O sessão está expirada, favor entrar em contato do equipe de desenvolvimento para renovar sessão")
        
        data_input: DadosEntradaFormatadosModel = DadosEntradaFormatadosModel(
            username=usuario,
            password=senha,
            footprint=cookie.conteudo,
            url_cookie=cookie.url,
            nome_responsavel="Marcelo Kowalski Teske",
            id_responsavel="23685",
            processo=fields.get("Processo").strip(),
            pasta=fields.get("Pasta").strip(),
            titulo=fields.get("Titulo").replace("-"," ").strip(),
            data_distribuicao=fields.get("DataDistribuicao").strip(),
            uf=fields.get("UF").strip(),
            cidade=fields.get("Cidade").strip(),
            orgao_julgador=fields.get("OrgaoJulgador").replace("-"," ").strip(),
            rito=fields.get("Rito").strip(),
            sistema_tribunal=fields.get("SistemaTribunal").strip(),
            nome_envolvido=fields.get("NomeEnvolvido").strip(),
            cpf_cnpj_envolvido=fields.get("CpfCnpjEnvolvido").strip(),
            arquivo_principal=fields.get("ArquivoPrincipal").strip(),
            houve_expedicao=fields.get("HouveExpedicao").strip() if fields.get("HouveExpedicao") else 'Nao',
            qualificacao_envolvido="Parte",
            processo_originario=fields.get("ProcessoOriginario") if fields.get("ProcessoOriginario") != '' and fields.get("ProcessoOriginario") is not None else fields.get("Processo"),
            natureza="CIVEL",
            fase="INICIAL",
            empresa="BOOKING.COM BRASIL SERVIÇOS DE RESERVA DE HOTÉIS LTDA",
            qualificacao_empresa="REU",
            situacao="ATIVO",
            descricao_objeto='Causa raiz:',
            portfolio='BOOKING',
            competencia='JUSTICA ESTADUAL',
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
        )

        data_input = CorrecaoErrosUsuarioUseCase(data_input=data_input).execute()

        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)

        return data_input