
def queryIniciarExecQueue(json_rec,virtual_host,queue):
    return """insert into queue 
                         (json_recebido,
                          virtual_host,
                          queue
                         ) 
                  values ('"""+str(json_rec)+"""',
                          '"""+str(virtual_host)+"""',
                          '"""+str(queue)+"""')"""