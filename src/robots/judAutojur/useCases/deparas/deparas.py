
class Deparas:
    def depara_posicao(posicao):
        depara = {
            "REU":"50",
            "Réu":"50",
            "Reu":"50",
            "Parte":"53",
            "PARTE":"53",
            "Autor":"16",
            "AUTOR":"16"
        }
        return depara.get(posicao) 