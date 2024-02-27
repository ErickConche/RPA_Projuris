
class Deparas:
    def depara_uf(uf):
        depara = {
            "São Paulo":"SP",
            "Paraná":"PR",
            "Minas Gerais":"MG",
            "Santa Catarina":"SC",
            "Goias":"GO",
            "Pernambuco":"PE",
            "Rio de Janeiro":"RJ",
            "Rio Grande do Norte":"RN",
            "Distrito Federal":"DF",
            "Rio Grande do Sul":"SC",
            "Espírito Santo":"ES",
            "Mato Grosso do Sul":"MS",
            "Mato Grosso":"MT",
            "Acre":"AC",
            "Alagoas":"AL",
            "Amapá":"AP",
            "Amazonas":"AM",
            "Bahia":"BA",
            "Ceará":"CE",
            "Maranhão":"MA",
            "Pará":"PA",
            "Paraíba":"PB",
            "Piauí":"PI",
            "Rondônia":"RO",
            "Roraima":"RR",
            "Sergipe":"SE",
            "Tocantins":"TO"
        }
        return depara.get(uf)
     
    def depara_autoridade(tipo_sistema):
        depara = {
            "PROCON":"27286",
            "PROCON / Consumidor.gov":"27287",
            "PROCON / Consumidor.gov.br":"27287"
        }
        return depara.get(tipo_sistema) 