
def ExisteCookieQueueQuery(queue: str):
    return """select * 
                from session_cookies
               where queue = '"""+queue+"""'"""