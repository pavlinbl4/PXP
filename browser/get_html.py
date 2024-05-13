import requests
from browser.curl import cookies, headers


def get_html_via_requests(url):
    response = requests.get(
        url,
        cookies=cookies,
        headers=headers,
    )
    if response.status_code == 200:
        return response.text
    print(f'{response.status_code = }')