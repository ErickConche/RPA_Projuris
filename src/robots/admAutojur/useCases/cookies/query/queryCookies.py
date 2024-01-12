
def QueryCookies(idcliente: int):
    return """select * 
                from cookies_autojur c 
               where idcliente = """+str(idcliente)+"""
               order by 1 desc;"""