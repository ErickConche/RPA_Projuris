
def queryBuscarQueue(virtual_host,
                     queue):
    return """select * 
                from queue qda
               where qda.finalizado <> true
                 and virtual_host = '"""+str(virtual_host)+"""'
                 and queue = '"""+str(queue)+"""'
               order by 1 """