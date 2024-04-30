class DeparaEstadoUfUseCase:
    def __init__(
            self,
            estado: str
        ) -> None:
        self.estado = estado
        self.depara = {
            "São Paulo":"SP",
            "Paraná":"PR",
            "Parana":"PR",
            "Minas Gerais":"MG",
            "Santa Catarina":"SC",
            "Goias":"GO",
            "Pernambuco":"PE",
            "Rio de Janeiro":"RJ",
            "Rio Grande do Norte":"RN",
            "Distrito Federal":"DF",
            "Rio Grande do Sul":"RS",
            "Espírito Santo":"ES",
            "Espirito Santo":"ES",
            "Mato Grosso do Sul":"MS",
            "Mato Grosso":"MT",
            "Acre":"AC",
            "Alagoas":"AL",
            "Amapá":"AP",
            "Amapa":"AP",
            "Amazonas":"AM",
            "Bahia":"BA",
            "Ceará":"CE",
            "Ceara":"CE",
            "Maranhão":"MA",
            "Pará":"PA",
            "Para":"PA",
            "Paraíba":"PB",
            "Paraíba":"PB",
            "Piauí":"PI",
            "Piaui":"PI",
            "Rondônia":"RO",
            "Rondonia":"RO",
            "Roraima":"RR",
            "Sergipe":"SE",
            "Tocantins":"TO"
        }

    def execute(self):
        return self.depara.get(self.estado)