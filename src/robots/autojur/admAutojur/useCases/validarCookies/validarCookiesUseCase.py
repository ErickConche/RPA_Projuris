import json
import requests
from bs4 import BeautifulSoup


class ValidarCookiesUseCase:
    def __init__(
        self,
        cookies_session: str
    ) -> None:
        self.cookies_session = cookies_session

    def execute(self) -> bool:
        try:
            cookies_list = json.loads(self.cookies_session)
            cookies_str = ''
            for cookie in cookies_list:
                cookies_str += f'{cookie.get("name")}={cookie.get("value")};'
            url = "https://baz.autojur.com.br/sistema/processos/processo.jsf"
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Cookie": cookies_str
            }
            response = requests.get(url=url, headers=headers)
            site_html = BeautifulSoup(response.text, 'html.parser')
            site_html.select_one("#form-pesquisa").find('input', {'name': 'javax.faces.ViewState'}).attrs.get('value')
            return True
        except Exception:
            return False
