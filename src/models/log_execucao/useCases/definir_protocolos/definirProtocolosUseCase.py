from time import sleep

class DefinirProtocolosUseCase:
    def __init__(
        self,
        queue: str,
        json_recebido: dict,
        json_enviado:dict = None,
    ) -> None:
        self.json_recebido = json_recebido
        self.json_enviado = json_enviado
        self.queue = queue
        self.protocolo1_recebido = ''
        self.protocolo2_recebido = ''
        self.protocolo_enviado = ''

    def execute(self):
        if 'adm-legalone' in self.queue:
            self.protocolo1_recebido = self.json_recebido.get("Fields").get("Reclamacao")
            if self.json_enviado:
                self.protocolo_enviado = self.json_enviado.get("Pasta")

        elif 'adm-autojur' in self.queue:
            self.protocolo1_recebido = self.json_recebido.get("Fields").get("Reclamacao")
            self.protocolo2_recebido = self.json_recebido.get("Fields").get("Pasta")
            if self.json_enviado:
                self.protocolo_enviado = self.json_enviado.get("Protocolo")

        elif 'jud-legalone' in self.queue:
            self.protocolo1_recebido = self.json_recebido.get("Fields").get("Processo")
            if self.json_enviado:
                self.protocolo_enviado = self.json_enviado.get("Pasta")

        elif 'jud-autojur' in self.queue:
            self.protocolo1_recebido = self.json_recebido.get("Fields").get("Processo")
            self.protocolo2_recebido = self.json_recebido.get("Fields").get("Pasta")
            if self.json_enviado:
                self.protocolo_enviado = self.json_enviado.get("Protocolo")
        
        return self.protocolo1_recebido, self.protocolo2_recebido, self.protocolo_enviado