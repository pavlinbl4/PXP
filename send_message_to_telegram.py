import requests
from dotenv import load_dotenv

from get_credentials import Credentials


def send_telegram_message(text: str):
    load_dotenv()
    token = Credentials().pavlinbl4_bot
    channel_id = Credentials().admin

    url = "https://api.telegram.org/bot"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": f"{text}"
    })

    if r.status_code != 200:
        raise Exception("post_text error")


if __name__ == '__main__':
    send_telegram_message('test message')
