
def QueryCookies(idcliente: int):
    return """select * 
                from cookies_autojur c 
               where idcliente = """+str(idcliente)+"""
                 and queue = 'app-jud-autojur'
               order by 1 desc;"""