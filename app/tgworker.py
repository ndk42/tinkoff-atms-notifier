import logging

import requests

from app.misc.consts import MAIN_LOGGER_NAME
from config import TELEGRAM_ACCESS_TOKEN

logger = logging.getLogger(f'{MAIN_LOGGER_NAME}.tworker')


class TelegramWorker:

    def __init__(self) -> None:
        pass

    _generate_api_url = 'https://api.telegram.org/bot{token}/{method}'.format

    def _send_raw_command(self, name: str, data: dict) -> requests.Response:
        api_url = self._generate_api_url(
            token=TELEGRAM_ACCESS_TOKEN,
            method=name
        )
        return requests.post(url=api_url, json=data)

    def send_message(self, text: str, chat_id: str, notify=True):
        try:
            return self._send_raw_command('sendMessage', {
                'text': text,
                'chat_id': chat_id,
                'parse_mode': 'markdown',
                'disable_notification': not notify})
        except Exception as e:
            logger.error(e)
