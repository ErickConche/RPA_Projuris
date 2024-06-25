
def ExisteCookieQueueQuery(queue: str, idcliente: int):
    return f"""select * 
                from session_cookies
               where queue = '{queue}'
                 and idcliente = {str(idcliente)}"""