
from typing import List
from unidecode import unidecode

from models.eventos_exp_jud.__model__.dadosEventosModel import DadosEventosModel


class Deparas:
    def __init__(self) -> None:
        pass

    def depara_responsavel(self, responsavel):
        depara = {
            "Paulo Gustavo Lukoff":"22689",
            "Luis Gustavo Silva":"29189",
            "Nathalia Ulanoski":"23682",
            "Bruna Veneski":"30739",
            "Isabella Dupim":"32166",
            "Isabella Rocha Dupim":"32166"
        }
        return depara.get(responsavel)

    def depara_evento(self, evento_busca, eventos: List[DadosEventosModel]):
        for evento in eventos:
            if unidecode(evento_busca.upper()) == unidecode(evento.nome_evento):
                return evento.id_evento
        return False
    
    def depara_usa_data_hora_evento(self, evento_busca, eventos: List[DadosEventosModel]):
        for evento in eventos:
            if unidecode(evento_busca.upper()) == unidecode(evento.nome_evento) and evento.usa_hora == True:
                return evento.id_evento
        return False