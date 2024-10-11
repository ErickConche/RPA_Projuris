from unidecode import unidecode
import re

def clean_string(value):
    return unidecode(re.sub(r'[^\w\s]', '', value)).lower()

def select_single(page, value):
    try:
        normalized_value = clean_string(value)
        options = page.query_selector_all('ul > li')
        options.reverse()

        for option in options:
            option_title = clean_string(option.get_attribute('title'))
            if normalized_value == option_title:
                option.click()
                break
    except Exception as e:
        raise Exception(f'Erro ao preencher dados, campo: {value}') from e

def select_option(page, name, value, index = 0):
    try:
        normalized_value = clean_string(value)
        selected = False
        options = page.query_selector_all('table > tbody > tr')

        if not options:
            return False

        for option in options:
            td_option = option.query_selector_all('td')[index]
            option_text = clean_string(td_option.inner_text())
            if normalized_value == option_text:
                option.dblclick()
                selected = True
                break
        return selected
    except Exception as e:
        raise Exception(f'Erro ao preencher dados, campo: {name}') from e
