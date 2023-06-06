import logging
import requests
from hikari.ilo import helpers
from hikari.config import Settings

settings = Settings()

class APIClient:
    def __init__(self, base_url, auth) -> None:
        self.base_url = base_url
        self.auth = auth
        self.actions = helpers.ActionsHelper(wrapper=self)

        self.logger = logging.getLogger("discord")

    def make_request(self, path, method="GET", params=None, data=None):

        url = f"{self.base_url}/{path}"

        try:
            response = requests.request(
                method,
                url,
                headers = {"Content-type": "application/json"},
                auth=(self.auth.username, self.auth.password),
                params=params,
                data=data,
                timeout=10,
                verify=settings.ilo.verify_ssl
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            self.logger.error("An error occurred during the HTTP request: %s", exc)

        return response


    def __getattr__(self, name):
        if name in ("get", "post", "put", "patch", "delete"):
            def method_wrapper(path, **kwargs):
                return self.make_request(path, method=name.upper(), **kwargs)
            return method_wrapper
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
