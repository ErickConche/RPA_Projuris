
import json
from modules.logger.Logger import Logger


class ValidarDadosEntradaUseCase:
    def __init__(
        self,
        classLogger: Logger,
        json_recebido: str
    ) -> None:
        self.classLogger = classLogger
        self.json_recebido = json_recebido

    def execute(self, type_robot) -> bool:
        message = "Iniciando validação dos campos de entrada"
        self.classLogger.message(message)
        json_recebido: dict = json.loads(self.json_recebido)
        fields: dict = json_recebido.get("Fields")
        credentials: dict = json_recebido.get('Credentials')

        if not credentials.get("Username") or not credentials.get("Password"):
            raise Exception("Dados de login incorretos")

        if 'Cível' in type_robot and not fields.get("TipoAcao"):
            raise Exception("Informe o tipo de ação")

        if not fields.get("Assunto"):
            raise Exception("Informe o assunto")

        if not fields.get("NomeEmpresa"):
            raise Exception("Informe o nome da empresa")

        if not fields.get("Unidade"):
            raise Exception("Informe a unidade")

        if not fields.get("Escritorio"):
            raise Exception("Informe o escritorio")

        if not fields.get("AdvogadoInterno"):
            raise Exception("Informe o advogado interno")

        if not fields.get("ParteContraria"):
            raise Exception("Informe a parte contrária")

        if not fields.get("CpfCnpjParteContraria"):
            raise Exception("Informe o cpf ou cnpj da parte contraria")

        if len(fields.get("CpfCnpjParteContraria")) != 14 and len(fields.get("CpfCnpjParteContraria")) != 11:
            raise Exception("CPF/CNPJ invalido")

        if not fields.get("Orgao"):
            raise Exception("Informe o orgão")

        if not fields.get("Comarca"):
            raise Exception("Informe a comarca")

        if not fields.get("Processo"):
            raise Exception("Informe o número do processo")

        if not fields.get("DataDistribuicao"):
            raise Exception("Informe a data de distribuição")

        if not fields.get("Juizo"):
            raise Exception("Informe o juízo")

        if not fields.get("DescricaoAssunto"):
            raise Exception("Informe a descrição do assunto")

        if not fields.get("pedido_1"):
            raise Exception("Informe o pedido 1")

        if not fields.get("valor_pedido_1"):
            raise Exception("Informe o valor do pedido 1")

        if not 'Cível' in type_robot and not fields.get("DataInicioVigencia"):
            raise Exception("Informe a data de início de vigência")

        if not fields.get("PrognosticoOriginal"):
            raise Exception("Informe o prognóstico original")

        if not fields.get("Inestimavel"):
            raise Exception("Informe o inestimável")

        if not fields.get("MoedaIndice"):
            raise Exception("Informe a moeda/índice")

        if not fields.get("Files"):
            raise Exception("Insira o arquivo")

        if fields.get("Litisconsorte") and not fields.get("DocumentoLitisconsorte"):
            raise Exception("Insira o documento do litisconsorte")

        message = "Fim da validação dos campos de entrada"
        self.classLogger.message(message)
        return True
