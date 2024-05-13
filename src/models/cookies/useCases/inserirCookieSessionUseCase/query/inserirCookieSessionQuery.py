
def InserirCookieSessionQuery(queue, cookie_session):
    return """insert into session_cookies (cookie, queue) 
                                   values ('"""+cookie_session+"""',
                                           '"""+queue+"""')
    """