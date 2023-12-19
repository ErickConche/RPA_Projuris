import psycopg2

class create_connect:
    def __init__(self,  
                 host:str,
                 port:str,
                 database:str,
                 user:str,
                 password:str)->None:
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def get_connect(self) -> str:
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        ) 