class DeparaEstadoCapitalUseCase:
    def __init__(
            self,
            uf: str
        ) -> None:
        self.uf = uf
        self.depara = {
            "AC": "RIO BRANCO",
            "AL": "MACEIO",
            "AP": "MACAPA",
            "AM": "MANAUS",
            "BA": "SALVADOR",
            "CE": "FORTALEZA",
            "DF": "BRASILIA",
            "ES": "VITORIA",
            "GO": "GOIANIA",
            "MA": "SAO LUIS",
            "MT": "CUIABA",
            "MS": "CAMPO GRANDE",
            "MG": "BELO HORIZONTE",
            "PA": "BELEM",
            "PB": "JOAO PESSOA",
            "PR": "CURITIBA",
            "PE": "RECIFE",
            "PI": "TERESINA",
            "RJ": "RIO DE JANEIRO",
            "RN": "NATAL",
            "RS": "PORTO ALEGRE",
            "RO": "PORTO VELHO",
            "RR": "BOA VISTA",
            "SC": "FLORIANOPOLIS",
            "SP": "SAO PAULO",
            "SE": "ARACAJU",
            "TO": "PALMAS"
        }

    def execute(self):
        return self.depara.get(self.uf)