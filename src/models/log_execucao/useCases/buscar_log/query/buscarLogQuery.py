
def buscarLogQuery(
    queue:str,
    protocolo1_recebido: str,
    protocolo2_recebido: str
):
    return f"""
        select * 
          from log_execucao le 
         where queue_execucao ilike '%{queue}%'
           and protocolo1_recebido = '{protocolo1_recebido}'
           and protocolo2_recebido = '{protocolo2_recebido}';
  """