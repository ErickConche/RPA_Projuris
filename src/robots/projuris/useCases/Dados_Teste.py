import os

dados_teste={
    "agencia_garantia": "0001",  # Docato
    "banco_garantia": "Bradesco",  # Docato
    "caso_acordo_condenacao": "Acordo",  # Docato
    "conta_garantia": "23232",  # Docato
    "data_inclusao": "13/03/2020",  # Docato
    "data_inclusao_doc": "13/05/2021",  # Docato
    "data_lancamento": "01/11/2023",  # Docato
    "data_liberacao": "08/12/2023",  # Docato
    "data_pagamento": "01/11/2021",  # Docato
    "data_pagamento_quitacoes": "13/11/2024",  # Docato
    "data_vencimento_lancamento": "07/12/2024",  # Docato
    "data_vencimento_quitacoes": "20/06/2023",  # Docato
    "devido_quitacoes": "2.323,00",  # Docato
    "depositada_pelo": "Despesa",  # Docato
    "documento_liberacao": "000111222333",  # Docato
    "garantia_tipo": "Penhora de Bens",  # Docato
    "identificador_garantia": "3",  # Docato
    "item_quitacao": "Objeto",  # Docato
    "juros_quitacoes": "",  # Docato
    "lancamento": "Custas Judiciais",  # Docato
    "metodo_atualizacao": "INPC",  # Docato
    "metodo_atualizacao_garantia": "IGP-M",  # Docato
    "motivo_liberacao": "Resgate",  # Docato
    "num_alvara": "123123123123",  # Docato
    "pago_condenacao": "50",  # Docato
    "parcela_garantia": "3",  # Docato
    "parcela_quitacoes": "2",  # Docato
    "principal_quitacoes": "2323",  # Docato
    "processo": "0000000-00.0000.0.00.0000",  # Docato
    "resgatado_por": "Cliente",  # Docato
    "sentenca_condenacao": "100",  # Docato
    "situacao_quitacoes": "Novo Pagamento",  # Docato
    "tipo_documento": "Doutrina",  # Docato
    "tipo_pagamento_quitacoes": "Alvará Judicial",  # Docato
    "valor_garantia": "567",  # Docato
    "valor_lancamento": "1523,00",  # Docato
    "valor_pago": "2.000,00",  # Docato
    "valor_pago_quitacoes": "25000",  # Docato
    "valor_resgatado": "123",  # Docato
    
    "contexto_atividade": "Custas", #dado analisado atraves da Docato

    "login": os.getenv("PROJURIS_LOGIN"), #dado fixo
    "senha": os.getenv("PROJURIS_SENHA"), #dado fixo
    "url": os.getenv("PROJURIS_URL"), #dado fixo

    "valor_lancamento_formatado": "", #dado tratado no código

    "primeiro_valor_custas": "",  #dado obtido no Projuris
    "segundo_valor_custas": "" #dado obtido no Projuris
}