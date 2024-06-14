from bs4 import BeautifulSoup
from unidecode import unidecode
from modules.logger.Logger import Logger
from datetime import datetime, timedelta


class ValidarTarefasUseCase:
    def __init__(
        self,
        evento: str,
        site_html: BeautifulSoup,
        classLogger: Logger
    ) -> None:
        self.site_html = site_html
        self.classLogger = classLogger
        self.evento = evento
        self.data_hora_agora = datetime.now()

    def execute(self):
        try:
            trs_agendamento = self.site_html.select_one("#tabview-pasta\\:aba-tarefa\\:form-tarefas\\:tabela_data").select("tr")
            for tr_agendamento in trs_agendamento:
                evento_encontrado = tr_agendamento.select(".lg-dado")[0].next
                data_lancamento_encontrado = datetime.strptime(tr_agendamento.select(".lg-dado")[4].next,'%d/%m/%Y %H:%M')
                diferenca_lancamento = self.data_hora_agora - data_lancamento_encontrado
                if diferenca_lancamento <= timedelta(days=7) and unidecode(evento_encontrado) == unidecode(self.evento):
                    message = f"Já existe um lançamento com a data {str(data_lancamento_encontrado)} para o evento {evento_encontrado}"
                    self.classLogger.message(message)
                    return True
        except Exception as error:
            message = f"Erro ao acessar validar tarefas"
            self.classLogger.message(message)
            raise error
    