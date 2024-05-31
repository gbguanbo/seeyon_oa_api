# -*- coding: utf-8 -*-


class BaseOAAPI:
    """WeChat API base class"""

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, **kwargs):
        if getattr(self, "api_base_url", None):
            kwargs["api_base_url"] = self.api_base_url
        return self._client.get(url, **kwargs)

    def _post(self, url, **kwargs):
        if getattr(self, "api_base_url", None):
            kwargs["api_base_url"] = self.api_base_url
        return self._client.post(url, **kwargs)

    @property
    def token(self):
        return self._client.token

    @property
    def session(self):
        return self._client.session

    @property
    def binding_user_session_id(self):
        return self._client.binding_user_session_id

    @property
    def binding_user_id(self):
        self.fetch_token()
        return self._client.binding_user_id_key
