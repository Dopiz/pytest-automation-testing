from urllib.parse import urljoin

from api.base_api import BaseAPI
from configurations import GamefiConfig


class GamefiAPI(BaseAPI):

    base_url = urljoin(GamefiConfig.BASE_URL, "gamefi/")

    GET_MINT_SIGN_PATH = "getMintSign"

    def mint_sign(self, miner_address: str, waiting_time: float = None):
        body = {
            'miner_address': miner_address
        }
        return self._send_request(
            method='POST',
            url=urljoin(self.base_url, self.GET_MINT_SIGN_PATH),
            json=body,
            waiting_time=waiting_time
        )
    
    ...