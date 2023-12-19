
def queryFinalizarExecQueue(id):
    return """update queue
                 set finalizado = true 
               where id = '"""+str(id)+"""'"""