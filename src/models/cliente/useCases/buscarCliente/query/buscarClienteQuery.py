
def BuscarClienteQuery(tenant):
    return """
    select * from cliente c 
       where c.tenant =  '"""+str(tenant)+"""';
  """