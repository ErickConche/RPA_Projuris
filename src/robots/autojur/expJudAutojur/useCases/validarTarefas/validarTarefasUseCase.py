from bs4 import BeautifulSoup
from unidecode import unidecode
from modules.logger.Logger import Logger
from datetime import datetime, timedelta
from modules.modularizacao.modularizacao import Modularizacao


class ValidarTarefasUseCase:
    def __init__(
        self,
        evento: str,
        site_html: BeautifulSoup,
        classLogger: Logger,
        data_final: str
    ) -> None:
        self.site_html = site_html
        self.classLogger = classLogger
        self.evento = evento
        self.data_hora_agora = datetime.now()
        self.qtde_dias_limite = 30
        self.data_final = data_final
        self.class_modularizacao = Modularizacao()

    def execute(self):
        try:
            if 'AUDIENCIA' in self.evento:
                print("Audiencia")
            trs_agendamento = self.site_html.select_one("#tabview-pasta\\:aba-tarefa\\:form-tarefas\\:tabela_data").select("tr")
            for tr_agendamento in trs_agendamento:
                evento_encontrado = tr_agendamento.select(".lg-dado")[0].next
                data_lancamento_encontrado = datetime.strptime(tr_agendamento.select(".lg-dado")[4].next,'%d/%m/%Y %H:%M')
                prazo_final_encontrado = tr_agendamento.select(".lg-dado")[3].next
                prazo_final, prazo_final_encontrado = self.class_modularizacao.modularizar_data(
                    self.data_final,
                    prazo_final_encontrado
                )
                diferenca_lancamento = self.data_hora_agora - data_lancamento_encontrado
                if (diferenca_lancamento <= timedelta(days=self.qtde_dias_limite) \
                    or prazo_final_encontrado == prazo_final) \
                    and unidecode(evento_encontrado) == unidecode(self.evento):
                    message = f"Indício de tarefa já cadastrada"
                    self.classLogger.message(message)
                    return True
        except Exception as error:
            message = f"Erro ao acessar validar tarefas"
            self.classLogger.message(message)
            raise error