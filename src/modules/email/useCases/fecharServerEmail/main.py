
class FecharServerEmail:
    
    def __init__(self,
                 server) -> None:
        self.server = server
        
    def execute(self):
        self.server.quit()
        return