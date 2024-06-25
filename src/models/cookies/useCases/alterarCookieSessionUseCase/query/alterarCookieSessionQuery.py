
def AlterarCookieSessionQuery(queue, cookie_session, idcliente):
    return f"""update session_cookies
                 set cookie = '{cookie_session}'
               where queue = '{queue}'
                 and idcliente = {str(idcliente)}
    """