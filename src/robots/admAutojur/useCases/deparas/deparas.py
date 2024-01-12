
class Deparas:
    def depara_autoridade(tipo_sistema):
        depara = {
            "PROCON":"27286",
            "PROCON / Consumidor.gov":"27287"
        }
        return depara.get(tipo_sistema) 