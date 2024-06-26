from robots.espaider.useCases.criarPartes.criarPartesUseCase import CriarPartesUseCase

def criar_parte(page, frame, data_input, value, classLogger, cpfcnpj):
    buttons = page.query_selector_all('.x-panel--toolbar.x-panel--toolbar-top > div > button')
    if not buttons:
        return False
    for button in buttons:
        if button.inner_text() != 'NOVO':
            continue
        button.click()
        page.wait_for_timeout(2000)
        CriarPartesUseCase(
            page=page,
            frame=frame,
            data_input=data_input, 
            classLogger=classLogger
        ).execute(value=value, cpfcnpj=cpfcnpj)
    frame.wait_for_timeout(2000)