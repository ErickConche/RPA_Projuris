from unidecode import unidecode

def select_single(page, value):
    try:
        options_ul = page.query_selector_all('ul > li')
        for option in options_ul:
            option_title_1 = unidecode(option.get_attribute('title')).lower()
            if value == option_title_1:
                option.dblclick()
                break
    except Exception as e:
        raise(f'Erro ao preencher dados, campo: {value}')

def select_option(page, name, value):
    try:
        selected = False
        options = page.query_selector_all('table > tbody > tr')
                
        if not options:
            raise(f'Erro ao preencher dados, campo: {name}')

        for option in options:
            td_option = option.query_selector('td')
            option_text_1 = unidecode(td_option.inner_text()).lower()
            if value == option_text_1:
                option.dblclick()
                selected = True
                break
        return selected
    except Exception as e:
        raise(f'Erro ao preencher dados, campo: {name}')