import json
from random import randint
from time import sleep

import requests

import tgworker
from misc.consts import NSK_REQUEST_JSON, TINKOFF_URL
from setup_logger import logger

from ..config import CLIENT_TELEGRAM_ID, CURRENCY_TO_SEARCH


class TinkoffNotifier:

    __slots__ = ('_currency',
                 '_request_json',
                 '_telegram_worker',
                 '_client_telegram_id')

    def __init__(self,
                 currency=CURRENCY_TO_SEARCH,
                 request_json=NSK_REQUEST_JSON,
                 client_tg_id=CLIENT_TELEGRAM_ID) -> None:

        self._currency = currency
        self._telegram_worker = tgworker.TelegramWorker()
        self._request_json = request_json
        self._client_telegram_id = client_tg_id

    def _make_atms_list(self, clusters: dict) -> list:
        return [
            {
                'address': point['address'],
                'limits': next(
                    x for x in point['limits']
                    if x['currency'] == self._currency
                    )
            } for cluster in clusters for point in cluster['points']]

    def run(self) -> None:

        prev_message = 'atms'
        while True:
            try:
                req = requests.post(url=TINKOFF_URL, json=self._request_json)

                repsonse_json = json.loads(req.content.decode('utf-8'))
                clusters = repsonse_json['payload']['clusters']

                atms_list = self._make_atms_list(clusters)
                message = ''

                for atm in atms_list:
                    message += str(atm['limits']['currency']) \
                        + str(atm['limits']['amount']) \
                        + ' avaliable at ' \
                        + atm['address'] \
                        + '\n'

                if message != '' and message != prev_message:
                    self._telegram_worker.send_message(
                        text=message,
                        chat_id=str(self._client_telegram_id)
                    )

                prev_message = message

            except Exception as e:
                logger.error(e)

            sleep(randint(58, 65))
