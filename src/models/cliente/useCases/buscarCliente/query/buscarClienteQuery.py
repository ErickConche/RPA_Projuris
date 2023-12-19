
def BuscarClienteQuery(tenant):
    return """
    select c.nome as nomecliente
          ,c.tenant
          ,s.nome as nomesistema
          ,s.url as urlsistema
          ,c2.usuario as usuariosistema
          ,c2.senha as senhasistema
     from cliente c 
    inner join sistemas_cliente sc on c.id = sc.idcliente 
    inner join sistema s on sc.idsistema = s.id 
    inner join credencial c2 on sc.idcredencial = c2.id 
    where c.tenant  = '"""+str(tenant)+"""'
      and c.ativo = true 
      and sc.ativo = true 
      and s.ativo = true 
      and c2.ativo = true
  """