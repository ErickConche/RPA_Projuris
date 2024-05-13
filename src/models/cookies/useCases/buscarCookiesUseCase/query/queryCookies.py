
def QueryCookies(idcliente: int, queue: str):
    return """select c.*,
                     sc.cookie as session_cookie
                from cookies_autojur c 
                left join session_cookies sc on sc.queue = c.queue
               where idcliente = '"""+str(idcliente)+"""'
                 and c.queue = '"""+str(queue)+"""'
               order by 1 desc;"""