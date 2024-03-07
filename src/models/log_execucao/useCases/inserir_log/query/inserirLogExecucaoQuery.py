
def InserirLogExecucaoQuery(
    queue_execucao:str,
    protocolo1_recebido:str,
    protocolo2_recebido:str,
    protocolo_enviado:str
):
    return f"""
        insert into log_execucao
			(queue_execucao,
			 protocolo1_recebido,
			 protocolo2_recebido,
			 protocolo_enviado
			)
	 values ('{queue_execucao}',
	 		 '{protocolo1_recebido}',
	 		 '{protocolo2_recebido}',
	 		 '{protocolo_enviado}');
    """