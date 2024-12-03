execution_login = False


def get_execution_login():
    global execution_login
    return execution_login


def update_execution_login(status: bool):
    global execution_login
    execution_login = status
