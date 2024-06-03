
from unidecode import unidecode


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
            unidecode("ALEGAÇÕES FINAIS"):"40",
            unidecode("ATO ORDINARIO"):"63",
            unidecode("ATO ORDINÁRIO"):"63",
            unidecode("AUDIÊNCIA DE CONCILIAÇÃO"):"70",
            unidecode('AUDIENCIA DE CONCILIACAO'):"70",
            unidecode("AUDIÊNCIA DE INSTRUÇÃO"):"72",
            unidecode("AUDIÊNCIA UNA"):"74",
            unidecode("CERTIDÃO"):"99",
            unidecode("CERTIDAO"):"99",
            unidecode("CITAÇÃO"):"106",
            unidecode("ALVARÁ EXPEDIDO"):"44",
            unidecode("CONTESTAÇÃO"):"137",
            unidecode("MANIFESTAÇÃO EMBARGOS DE DECLARACAO"):"304",
            unidecode('MANIFESTACAO EMBARGOS DE DECLARACAO'):"304",
            unidecode("CONTRARRAZÕES JEC"):"144",
            unidecode("CONTRARRAZOES JEC"):"144",
            unidecode("CONTRA RAZÕES"):"140",
            unidecode("CONTRA RAZOES"):"140",
            unidecode("PROCESSO ARQUIVADO"):"415",
            unidecode("PENHORA"):"392",
            unidecode("COMPROVAR PAGAMENTO"):"123",
            unidecode("PRESTAR INFORMAÇÕES"):"412",
            unidecode("IMPUGNAÇÃO AO CUMPRIMENTO DE SENTENÇA"):"246",
            unidecode("MANIFESTACAO"):"302",
            unidecode("DESPACHO"):"180",
            unidecode("BLOQUEIO BACEN"):"84",
            unidecode("EXECUÇÃO DE SENTENÇA"):"224",
            unidecode("DOCUMENTOS"):"190",
            unidecode("INTIMAÇÃO"):"266",
            unidecode("EFETUAR PAGAMENTO"):"196",
            unidecode("MIGRAÇÃO"):"313",
            unidecode("MANIFESTAÇÃO"):"302",
            unidecode("MANIFESTACAO"):"302",
            unidecode("MANIFESTAÇÃO SOBRE PROVAS A PRODUZIR"):"309",
            unidecode("OFÍCIO RECEBIDO"):"373",
            unidecode("SENTENÇA PUBLICADA"):"510",
            unidecode("SENTENCA PUBLICADA"):"510",
            unidecode("SENTENÇA HOMOLOGATÓRIA"):"508",
            unidecode("MANIFESTACAO SOBRE PROVAS A PRODUZIR"):"309",
            unidecode("MANIFESTACAO SOBRE O RETORNO DOS AUTOS"):"308",
            unidecode('MANIFESTAÇÃO SOBRE O RETORNO DOS AUTOS'):"308",
            unidecode("INCLUSÃO EM PAUTA"):"249",
            unidecode("INCLUSAO EM PAUTA"):"249",
            unidecode("EXTINÇÃO DO PROCESSO"):"230"
        }
        return depara.get(unidecode(evento)) 
    
    def depara_usa_data_hora_evento(self, evento):
        depara = {
            unidecode("ALEGAÇÕES FINAIS"):"40",
            unidecode("AUDIÊNCIA DE CONCILIAÇÃO"):"70",
            unidecode("AUDIENCIA DE CONCILIACAO"):"70",
            unidecode("AUDIÊNCIA DE INSTRUÇÃO"):"72",
            unidecode("AUDIÊNCIA UNA"):"74",
            unidecode("CONTESTAÇÃO"):"137",
            unidecode("MANIFESTAÇÃO EMBARGOS DE DECLARACAO"):"304",
            unidecode("MANIFESTACAO EMBARGOS DE DECLARACAO"):"304",
            unidecode("CONTRARRAZÕES JEC"):"144",
            unidecode("CONTRARRAZOES JEC"):"144",
            unidecode("MANIFESTAÇÃO"):"302",
            unidecode("MANIFESTACAO"):"302",
            unidecode("CONTRA RAZÕES"):"140",
            unidecode("CONTRA RAZOES"):"140",
            unidecode("COMPROVAR PAGAMENTO"):"123",
            unidecode("PRESTAR INFORMAÇÕES"):"412",
            unidecode("IMPUGNAÇÃO AO CUMPRIMENTO DE SENTENÇA"):"246",
            unidecode("MANIFESTACAO"):"302",
            unidecode("EXECUÇÃO DE SENTENÇA"):"224",
            unidecode("MANIFESTAÇÃO SOBRE PROVAS A PRODUZIR"):"309",
            unidecode("MANIFESTACAO SOBRE PROVAS A PRODUZIR"):"309",
            unidecode("MANIFESTACAO SOBRE O RETORNO DOS AUTOS"):"308",
            unidecode("MANIFESTAÇÃO SOBRE O RETORNO DOS AUTOS"):"308"
        }
        return depara.get(unidecode(evento))