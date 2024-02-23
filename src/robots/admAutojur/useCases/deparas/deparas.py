
class Deparas:
    def depara_uf(uf):
        depara = {
            "São Paulo":"SP",
            "Paraná":"PR",
            "Minas Gerais":"MG",
            "Santa Catarina":"SC",
            "Goias":"GO"
        }
        return depara.get(uf)
     
    def depara_autoridade(tipo_sistema):
        depara = {
            "PROCON":"27286",
            "PROCON / Consumidor.gov":"27287",
            "PROCON / Consumidor.gov.br":"27287"
        }
        return depara.get(tipo_sistema) 