import json
from datetime import datetime
from modules.logger.Logger import Logger
from modules.formatacao.formatacao import Formatacao
from robots.espaider.useCases.formatarDadosEntrada.__model__.dadosEntradaEspaiderModel import (
    DadosEntradaEspaiderModel)
from models.cookies.cookiesUseCase import CookiesUseCase
from models.cliente.__model__.ClienteModel import ClienteModel


class FormatarDadosEntradaUseCase:
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

    def execute(self) -> DadosEntradaEspaiderModel:
        json_recebido: dict = json.loads(self.json_recebido)
        fields: dict = json_recebido.get("Fields")
        credentials: dict = json_recebido.get('Credentials')
        current_time = datetime.now().strftime("%d/%m/%Y")

        data_input: DadosEntradaEspaiderModel = DadosEntradaEspaiderModel(
            footprint="",
            url_cookie="",
            cookie_session="",
            username=credentials.get("Username"),
            password=credentials.get("Password"),
            fase="Conhecimento" if self.robot in ['Cível', 'Trabalhista'] else "Inicial",
            natureza=fields.get("Natureza") if fields.get(
                "Natureza") else "Judicial",
            categoria=fields.get("Categoria") if fields.get("Categoria") else self.robot,
            tipo_acao=fields.get("TipoAcao") if fields.get(
                "TipoAcao") else "Reclamação trabalhista",
            assunto=fields.get("Assunto") if self.robot in ['Cível', 'Autos'] else "",
            contingencia=fields.get("Contingencia") if fields.get(
                "Contingencia") else "Passiva",
            # NumeroRastreio=fields.get("NumeroRastreio"),
            empresa=fields.get("NomeEmpresa"),
            unidade=fields.get("Unidade"),
            condicao=fields.get("CondicaoCliente") if fields.get(
                "CondicaoCliente") else "Réu",
            escritorio=fields.get("Escritorio"),
            advogado=fields.get("AdvogadoInterno"),
            parte_contraria=fields.get("ParteContraria"),
            # CentroCusto=fields.get(
            #     "CentroCusto") if self.robot == 'Trabalhista' else "",
            cpf_cnpj_parte_contraria=fields.get("CpfCnpjParteContraria"),
            litisconsorte=fields.get("Litisconsorte"),
            orgao=fields.get("Orgao"),
            comarca=fields.get("Comarca"),
            processo=fields.get("Processo"),
            data_distribuicao=fields.get("DataDistribuicao"),
            juizo=fields.get("Juizo"),
            instancia='1ª Instância',
            peticionamento=fields.get("Peticionamento") if fields.get(
                "Peticionamento") else "Eletrônico",
            descricao_assunto=fields.get("DescricaoAssunto"),
            pedido_1=fields.get("pedido_1"),
            valor_pedido_1=fields.get("valor_pedido_1") if fields.get(
                "pedido_1") else '0,00',
            data_base_calculo=fields.get("DataDistribuicao"),
            data_inicio_vigencia=fields.get("DataInicioVigencia") if fields.get(
                "DataInicioVigencia") else current_time,
            data_inicio_contabil=fields.get("DataDistribuicao"),
            risco_original=fields.get("PrognosticoOriginal"),
            inestimavel=fields.get("Inestimavel"),
            moeda_indice=fields.get("MoedaIndice"),
            juros='0,00' if fields.get("MoedaIndice") == "SELIC" else '1,00',
            desdobramento="Ação de Repetição de Indébito",
            classe_partes="Litisconsorte",
            # Regra="Sobre Principal e Multa",
            # ValorTributo=fields.get("ValorTributo"),
            # ValorMulta=fields.get("ValorMulta"),
            # ValorJuros=fields.get("ValorJuros"),
            nome_documento="Íntegra do processo",
            data_documento=fields.get("DataDistribuicao"),
            file=fields.get("Files") if fields.get("Files") else "",
            parte_contraria_1=fields.get("parte_contraria_1") if fields.get("parte_contraria_1") else "",
            cpf_cnpj_parte_processo_1=fields.get("cpf_cnpj_parte_processo_1") if fields.get("parte_contraria_1") else "",
            condicao_parte_processo_1=fields.get("condicao_parte_processo_1") if fields.get("parte_contraria_1") else "",
            parte_contraria_2=fields.get("parte_contraria_1") if fields.get("parte_contraria_2") else "",
            cpf_cnpj_parte_processo_2=fields.get("cpf_cnpj_parte_processo_1") if fields.get("parte_contraria_2") else "",
            condicao_parte_processo_2=fields.get("condicao_parte_processo_1") if fields.get("parte_contraria_2") else "",
            parte_contraria_3=fields.get("parte_contraria_1") if fields.get("parte_contraria_3") else "",
            cpf_cnpj_parte_processo_3=fields.get("cpf_cnpj_parte_processo_1") if fields.get("parte_contraria_3") else "",
            condicao_parte_processo_3=fields.get("condicao_parte_processo_1") if fields.get("parte_contraria_3") else "",
            parte_contraria_4=fields.get("parte_contraria_1") if fields.get("parte_contraria_4") else "",
            cpf_cnpj_parte_processo_4=fields.get("cpf_cnpj_parte_processo_1") if fields.get("parte_contraria_4") else "",
            condicao_parte_processo_4=fields.get("condicao_parte_processo_1") if fields.get("parte_contraria_4") else "",
            parte_contraria_5=fields.get("parte_contraria_1") if fields.get("parte_contraria_5") else "",
            cpf_cnpj_parte_processo_5=fields.get("cpf_cnpj_parte_processo_1") if fields.get("parte_contraria_5") else "",
            condicao_parte_processo_5=fields.get("condicao_parte_processo_1") if fields.get("parte_contraria_5") else "",
            pedido_2=fields.get("pedido_2") if fields.get("pedido_2") else "",
            valor_pedido_2=fields.get("valor_pedido_2") if fields.get("pedido_2") else "",
            pedido_3=fields.get("pedido_3") if fields.get("pedido_3") else "",
            valor_pedido_3=fields.get("valor_pedido_3") if fields.get("pedido_3") else "",
            pedido_4=fields.get("pedido_4") if fields.get("pedido_4") else "",
            valor_pedido_4=fields.get("valor_pedido_4") if fields.get("pedido_4") else "",
            pedido_5=fields.get("pedido_5") if fields.get("pedido_5") else "",
            valor_pedido_5=fields.get("valor_pedido_5") if fields.get("pedido_5") else "",
            pedido_6=fields.get("pedido_6") if fields.get("pedido_6") else "",
            valor_pedido_6=fields.get("valor_pedido_6") if fields.get("pedido_6") else "",
            pedido_7=fields.get("pedido_7") if fields.get("pedido_7") else "",
            valor_pedido_7=fields.get("valor_pedido_7") if fields.get("pedido_7") else "",
            pedido_8=fields.get("pedido_8") if fields.get("pedido_8") else "",
            valor_pedido_8=fields.get("valor_pedido_8") if fields.get("pedido_8") else "",
            pedido_9=fields.get("pedido_9") if fields.get("pedido_9") else "",
            valor_pedido_9=fields.get("valor_pedido_9") if fields.get("pedido_9") else "",
            pedido_10=fields.get("pedido_10") if fields.get("pedido_10") else "",
            valor_pedido_10=fields.get("valor_pedido_10") if fields.get("pedido_10") else "",
            pedido_11=fields.get("pedido_11") if fields.get("pedido_11") else "",
            valor_pedido_11=fields.get("valor_pedido_11") if fields.get("pedido_11") else "",
            pedido_12=fields.get("pedido_12") if fields.get("pedido_12") else "",
            valor_pedido_12=fields.get("valor_pedido_12") if fields.get("pedido_12") else "",
            pedido_13=fields.get("pedido_13") if fields.get("pedido_13") else "",
            valor_pedido_13=fields.get("valor_pedido_13") if fields.get("pedido_13") else "",
            pedido_14=fields.get("pedido_14") if fields.get("pedido_14") else "",
            valor_pedido_14=fields.get("valor_pedido_14") if fields.get("pedido_14") else "",
            pedido_15=fields.get("pedido_15") if fields.get("pedido_15") else "",
            valor_pedido_15=fields.get("valor_pedido_15") if fields.get("pedido_15") else "",
            pedido_16=fields.get("pedido_16") if fields.get("pedido_16") else "",
            valor_pedido_16=fields.get("valor_pedido_16") if fields.get("pedido_16") else "",
            pedido_17=fields.get("pedido_17") if fields.get("pedido_17") else "",
            valor_pedido_17=fields.get("valor_pedido_17") if fields.get("pedido_17") else "",
            pedido_18=fields.get("pedido_18") if fields.get("pedido_18") else "",
            valor_pedido_18=fields.get("valor_pedido_18") if fields.get("pedido_18") else "",
            pedido_19=fields.get("pedido_19") if fields.get("pedido_19") else "",
            valor_pedido_19=fields.get("valor_pedido_19") if fields.get("pedido_19") else "",
            pedido_20=fields.get("pedido_20") if fields.get("pedido_20") else "",
            valor_pedido_20=fields.get("valor_pedido_20") if fields.get("pedido_20") else "",
            pedido_21=fields.get("pedido_21") if fields.get("pedido_21") else "",
            valor_pedido_21=fields.get("valor_pedido_21") if fields.get("pedido_21") else "",
            pedido_22=fields.get("pedido_22") if fields.get("pedido_22") else "",
            valor_pedido_22=fields.get("valor_pedido_22") if fields.get("pedido_22") else "",
            pedido_23=fields.get("pedido_23") if fields.get("pedido_23") else "",
            valor_pedido_23=fields.get("valor_pedido_23") if fields.get("pedido_23") else "",
            pedido_24=fields.get("pedido_24") if fields.get("pedido_24") else "",
            valor_pedido_24=fields.get("valor_pedido_24") if fields.get("pedido_24") else "",
            pedido_25=fields.get("pedido_25") if fields.get("pedido_25") else "",
            valor_pedido_25=fields.get("valor_pedido_25") if fields.get("pedido_25") else "",
            pedido_26=fields.get("pedido_26") if fields.get("pedido_26") else "",
            valor_pedido_26=fields.get("valor_pedido_26") if fields.get("pedido_26") else "",
            pedido_27=fields.get("pedido_27") if fields.get("pedido_27") else "",
            valor_pedido_27=fields.get("valor_pedido_27") if fields.get("pedido_27") else "",
            pedido_28=fields.get("pedido_28") if fields.get("pedido_28") else "",
            valor_pedido_28=fields.get("valor_pedido_28") if fields.get("pedido_28") else "",
            pedido_29=fields.get("pedido_29") if fields.get("pedido_29") else "",
            valor_pedido_29=fields.get("valor_pedido_29") if fields.get("pedido_29") else "",
            pedido_30=fields.get("pedido_30") if fields.get("pedido_30") else "",
            valor_pedido_30=fields.get("valor_pedido_30") if fields.get("pedido_30") else "",
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
