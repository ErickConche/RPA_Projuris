from datetime import datetime
import json
from modules.logger.Logger import Logger
from models.cookies.cookiesUseCase import CookiesUseCase
from models.cliente.__model__.ClienteModel import ClienteModel
from modules.decodePassword.decodePassword import DecodePassword
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderCadastroModel import (
    DadosEntradaEspaiderCadastroModel)


class formatarDadosEntradaCadastroUseCase:
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

    def execute(self) -> DadosEntradaEspaiderCadastroModel:
        json_recebido: dict = json.loads(self.json_recebido)
        fields: dict = json_recebido.get("Fields")
        credentials: dict = json_recebido.get('Credentials')
        credentials['Username'] = 'C0692082'
        credentials['Password'] = 'doc@to2024'
        current_time = datetime.now().strftime("%d/%m/%Y")
        alerta_prazo = datetime.strptime(fields.get("AlertaPrazoAudiencia"), "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y") if fields.get("AlertaPrazoAudiencia") else None

        data_input: DadosEntradaEspaiderCadastroModel = DadosEntradaEspaiderCadastroModel(
            footprint="",
            url_cookie="",
            cookie_session="",
            username=credentials.get("Username"),
            password=DecodePassword(classLogger=self.classLogger, password=credentials.get("Password")).decrypt(),
            natureza=fields.get("Natureza") or '',
            tipo_acao=fields.get("TipoAcao") or '',
            cliente_principal=fields.get("Cliente") or '',
            condicao_cliente=fields.get("CondicaoCliente") or '',
            adverso_principal=fields.get("AdversoPrincipal") or '',
            condição_adverso=fields.get("CondicaoAdverso") or '',
            advogado_interno_vale=fields.get("AdvogadoInterno") or '',
            documento_adverso_principal=fields.get("DocumentoAdversoPrincipal"),
            tipo=fields.get("Tipo") or '',
            unidade_centralizadora=fields.get("UnidadeCentralizadora") or '',
            situacao=fields.get("Situacao") or '',
            escritorio=fields.get("Escritorio") or '',
            valor_da_causa=fields.get("ValorCausa") or '',
            desdobramento=fields.get("Desdobramento") or '',
            procedimento=fields.get("Procedimento") or '',
            instancia='1ª Instância',
            orgao=fields.get("Orgao") or '',
            juizo=fields.get("Vara"),
            comarca=fields.get("Comarca") or '',
            numero_do_processo=fields.get("Processo") or fields.get("ProcessoPreCadastro"),
            numero_processo_pre_cadastro=fields.get("ProcessoPreCadastro") or '',
            advogado_adverso=fields.get("AdvogadoAdverso") or '',
            documento_advogado_adverso=fields.get("DocumentoAdvogadoAdverso"),
            documento_cliente_principal=fields.get("DocumentoClientePrincipal") or '',
            tipo_audiencia=fields.get("TipoAudiencia") or '',
            modalidade=fields.get("Modalidade") or '',
            alerta_prazo_audiencia=alerta_prazo,
            vara=fields.get("Vara"),
            data_andamento=fields.get("DataAndamento1") or '',
            distribuido_em=fields.get("DataDistribuicao") or current_time,
            audiencia_designada=fields.get("AudienciaDesignada") or '',
            hora_audiencia=fields.get("HoraAudiencia") or '',
            arquivo=fields.get("Documento"),
            acao_especial="Em Cadastramento",
            unidade_controle="Em Cadastramento",
            status="Ativo",
            houve_discussao_anterior="Não",
            envolve_base_metais="Não",
            estrategico="Não",
            complexo='N/A',
            mina_unidade='N/A',
            nome_assunto='Inicial',
            tipo_documento='Inicial',
            em_andamento='Audiência',
            providencia_audiencia='Indicação de preposto',
            responsavel_audiencia='Em Cadastramento',
            status_audiencia='Designada',
            andamento='Distribuição'
        )

        cookie = CookiesUseCase(
            con_rd=self.con_rd
        ).buscarCookies(
            queue=self.queue,
            idcliente=self.cliente.id
        )

        if cookie:
            data_input.footprint = cookie.conteudo
            data_input.url_cookie = cookie.url
            data_input.cookie_session = cookie.session_cookie

        message = "Fim da formatação dos campos de entrada"
        self.classLogger.message(message)

        return data_input
