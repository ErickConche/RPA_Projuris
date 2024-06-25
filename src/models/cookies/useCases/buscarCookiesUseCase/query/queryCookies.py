
def QueryCookies(idcliente: int, queue: str):
    return f"""select ca.*,
	                   sc.cookie as session_cookie 
                from cliente c 
               left join session_cookies sc on c.id = sc.idcliente 
               left join cookies_autojur ca on c.id = ca.idcliente
              where c.id = {str(idcliente)}
                and (sc.queue = '{queue}' or ca.queue = '{queue}')
               order by 1 desc;"""