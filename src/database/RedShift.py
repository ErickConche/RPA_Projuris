import redshift_connector

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
        return redshift_connector.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        ) 