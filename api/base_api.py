import json

import requests

from configurations import GeneralConfig


class BaseAPI:

    def __init__(self, env_flag=None, waiting_time=None):
        self.env_flag = env_flag or None
        self.waiting_time = waiting_time or GeneralConfig.API_ACCEPTABLE_WAITING_TIME
        self._session = requests.Session()

    def _send_request(self, method: str, url: str, **kwargs):
        acceptable_waiting_time = kwargs.pop('waiting_time', None) or self.waiting_time
        try:
            response = self._session.request(method, url, **kwargs)
            # print("Response:\n" + json.dumps(response.json(), indent=4, ensure_ascii=False))
            duration = response.elapsed.total_seconds()
            assert duration <= acceptable_waiting_time, (
                f"Response Time > {acceptable_waiting_time}s, Actual: {duration}s")
        except requests.exceptions.RequestException as e:
            response = None
            print(f"Request Error | url: [{method}] {url}, kwargs: {kwargs}, error: {str(e)}")
        return response
