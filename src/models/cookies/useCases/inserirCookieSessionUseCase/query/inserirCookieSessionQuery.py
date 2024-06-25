
def InserirCookieSessionQuery(queue, cookie_session, idcliente):
    return f"""insert into session_cookies (cookie, queue, idcliente) 
                                   values ('{cookie_session}',
                                           '{queue}',
                                           '{str(idcliente)}');
    """