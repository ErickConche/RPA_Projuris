from unidecode import unidecode

def insert_value(data_input, de_para, name, frame, tag="name"):
    try:
        value = getattr(data_input, de_para[name])
        value = unidecode(value).lower()
        input = frame.wait_for_selector(f'[{tag}={name}]')
        if name == 'ABA_DESD_JuizoIDEdt':
            value = value.replace('civil', 'civel')
        input.fill(value)
        return value
    except Exception as e:
        raise(f'Erro ao preencher dados, campo: {name}')