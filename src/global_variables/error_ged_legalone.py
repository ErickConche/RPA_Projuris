error_ged_legalone = False

def get_error_ged_legalone():
    global error_ged_legalone
    return error_ged_legalone

def update_error_ged_legalone(status: bool):
    global error_ged_legalone
    error_ged_legalone = status
