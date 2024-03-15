
class Deparas:
    def depara_posicao_reclamante(reclamante):
        depara = {
            "Empresa":"1",
            "Reclamante":"6",
            "Responsável":"4"
        }
        return depara.get(reclamante)
    
    def depara_sistema(sistema):
        depara = {
            "Notificação Extrajudicial":"17",
            "Ofício":"16",
            "PROCON":"13",
            "PROCON / Consumidor.gov.br":"15",
            "PROCON / Proconsumidor":"14",
            'PROCON-Consumidorgovbr':"15"
        }
        return depara.get(sistema)
    
    def depara_tipo_processo(tipoprocesso):
        depara = {
            "C.I.P.":"3",
            "C.I.P":"3",
            "F.A.":"4",
            "Processo Administrativo":"6",
            "Reclamação":"5",
            "Recurso Administrativo":"7"
        }
        return depara.get(tipoprocesso)
    
    def depara_tipo_reclamacao(tiporeclamacao):
        depara = {
            "Digital":"2",
            "Física":"1"
        }
        return depara.get(tiporeclamacao)