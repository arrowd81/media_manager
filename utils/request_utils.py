import logging
import time

import requests


def safe_request(method, path, retries: int = 5, **kwargs):
    default_error = requests.RequestException()
    for _ in range(retries):
        try:
            response = requests.request(method, path, **kwargs)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.info(f"request error: {e}")
            default_error = e
            time.sleep(1)
        else:
            return response
    raise default_error
