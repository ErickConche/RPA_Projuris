
class Deparas:
    def depara_posicao_outros_envolvidos(posicao):
        depara = {
            "Advogado contrário":"19",
            "Autor":"1",
            "CAPITAL O PIRATININGA HOTEL":"22",
            "Chamado ao processo":"7",
            "Contador":"8",
            "Denunciado da lide":"9",
            "Interessado":"10",
            "Juiz":"11",
            "Nomeado à autoria":"12",
            "Opositor":"13",
            "Perito":"14",
            "Preposto":"15",
            "Representante":"23",
            "Réu":"2",
            "Sim":"24",
            "Solicitante":"20",
            "Subestabelecido":"17",
            "Testemunha":"18"
        }
        return depara.get(posicao)
    
    def depara_situacao_outros_envolvidos(situacao):
        depara = {
            "Empresa":"0",
            "Responsável":"1",
            "Contrário":"2",
            "Parte":"3",
            "Outros":"4",
            "Advogado contrário":"5",
            "Correspondente":"7"
        }
        return depara.get(situacao)
                                          
    def depara_acao(acao):
        depara = {
            "Indenizatória":"17",
            "Indenizatoria":"17",
            "Cumprimento de Sentença.":"74",
            "Reclamação Pré-Processual":"93",
            "Carta Precatória.":"87"
        }
        return depara.get(acao)
    
    def depara_natureza(natureza):
        depara = {
            "Cível":"2",
            "Civel":"2"
        }
        return depara.get(natureza)
    
    def depara_fase(fase):
        depara = {
            "Inicial":"9",
            "Pré-processual":"10"
        }
        return depara.get(fase)
    
    def depara_procedimento(procedimento):
        depara = {
            "Especial":"1",
            "Comum":"6",
            "Pré-Processual":"7"
        }
        return depara.get(procedimento)
    
    def depara_justica(justica):
        depara = {
            "Justiça do Trabalho":"15",
            "Justiça Eleitoral":"17",
            "Justiça Estadual":"13",
            "Justiça Federal":"14",
            "Justiça Militar":"15"
        }
        return depara.get(justica)
    