
def queryIniciarElementoExecQueue(id):
    return """update queue
                 set executando = true 
               where id = '"""+str(id)+"""'"""