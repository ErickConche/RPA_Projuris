
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

    def depara_evento(self, evento):
        depara = {
            "ALEGAÇÕES FINAIS":"40",
            "ATO ORDINARIO":"63",
            "ATO ORDINÁRIO":"63",
            "AUDIÊNCIA DE CONCILIAÇÃO":"70",
            "AUDIÊNCIA DE INSTRUÇÃO":"72",
            "AUDIÊNCIA UNA":"74",
            "CERTIDÃO":"99",
            "CITAÇÃO":"106",
            "ALVARÁ EXPEDIDO":"44",
            "CONTESTAÇÃO":"137",
            "MANIFESTAÇÃO EMBARGOS DE DECLARACAO":"304",
            'MANIFESTACAO EMBARGOS DE DECLARACAO':"304",
            "CONTRARRAZÕES JEC":"144",
            "CONTRARRAZOES JEC":"144",
            "CONTRA RAZÕES":"140",
            "CONTRA RAZOES":"140",
            "PROCESSO ARQUIVADO":"415",
            "PENHORA":"392",
            "COMPROVAR PAGAMENTO":"123",
            "PRESTAR INFORMAÇÕES":"412",
            "IMPUGNAÇÃO AO CUMPRIMENTO DE SENTENÇA":"246",
            "MANIFESTACAO":"302",
            "DESPACHO":"180",
            "BLOQUEIO BACEN":"84",
            "EXECUÇÃO DE SENTENÇA":"224",
            "DOCUMENTOS":"190",
            "INTIMAÇÃO":"266",
            "EFETUAR PAGAMENTO":"196",
            "MIGRAÇÃO":"313",
            "MANIFESTAÇÃO":"302",
            "MANIFESTACAO":"302",
            "MANIFESTAÇÃO SOBRE PROVAS A PRODUZIR":"309",
            "OFÍCIO RECEBIDO":"373",
            "SENTENÇA PUBLICADA":"510",
            "SENTENÇA HOMOLOGATÓRIA":"508",
            "MANIFESTACAO SOBRE PROVAS A PRODUZIR":"309",
            "MANIFESTACAO SOBRE O RETORNO DOS AUTOS":"308",
            'MANIFESTAÇÃO SOBRE O RETORNO DOS AUTOS':"308",
            "INCLUSÃO EM PAUTA":"249",
            "INCLUSAO EM PAUTA":"249",
            "EXTINÇÃO DO PROCESSO":"230"
        }
        return depara.get(evento) 
    
    def depara_usa_data_hora_evento(self, evento):
        depara = {
            "ALEGAÇÕES FINAIS":"40",
            "AUDIÊNCIA DE CONCILIAÇÃO":"70",
            "AUDIÊNCIA DE INSTRUÇÃO":"72",
            "AUDIÊNCIA UNA":"74",
            "CONTESTAÇÃO":"137",
            "MANIFESTAÇÃO EMBARGOS DE DECLARACAO":"304",
            'MANIFESTACAO EMBARGOS DE DECLARACAO':"304",
            "CONTRARRAZÕES JEC":"144",
            "CONTRARRAZOES JEC":"144",
            "MANIFESTAÇÃO":"302",
            "MANIFESTACAO":"302",
            "CONTRA RAZÕES":"140",
            "CONTRA RAZOES":"140",
            "COMPROVAR PAGAMENTO":"123",
            "PRESTAR INFORMAÇÕES":"412",
            "IMPUGNAÇÃO AO CUMPRIMENTO DE SENTENÇA":"246",
            "MANIFESTACAO":"302",
            "EXECUÇÃO DE SENTENÇA":"224",
            "MANIFESTAÇÃO SOBRE PROVAS A PRODUZIR":"309",
            "MANIFESTACAO SOBRE PROVAS A PRODUZIR":"309",
            "MANIFESTACAO SOBRE O RETORNO DOS AUTOS":"308",
            'MANIFESTAÇÃO SOBRE O RETORNO DOS AUTOS':"308",
        }
        return depara.get(evento)