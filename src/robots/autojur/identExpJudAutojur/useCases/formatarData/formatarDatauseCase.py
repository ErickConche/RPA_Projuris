from datetime import datetime

def formatarData(data):
    data = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%fZ")
    return data.strftime("%d/%m/%Y")