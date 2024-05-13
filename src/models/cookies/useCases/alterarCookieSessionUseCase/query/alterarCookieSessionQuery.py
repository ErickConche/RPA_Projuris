
def AlterarCookieSessionQuery(queue, cookie_session):
    return """update session_cookies
                 set cookie = '"""+cookie_session+"""'
               where queue = '"""+queue+"""'
    """