# -*- coding: utf-8 -*-


import time

from ..client.base import BaseOAClient
from ..client import api


class OAClient(BaseOAClient):

    bpm = api.OABPM()
    bulletins = api.OABulletins()
    file = api.OAFile()
    org = api.OAOrg()

    def __init__(
        self,
        api_base_url,
        rest_account, rest_password, login_name, token=None, session=None, timeout=None, auto_retry=True
    ):
        super().__init__(api_base_url,rest_account, rest_password, login_name, token, session, timeout, auto_retry)
        self.api_base_url = api_base_url
        self.rest_account = rest_account
        self.rest_password = rest_password 
        self.login_name = login_name


    def fetch_token(self):
        return self._fetch_token(
            url=self.api_base_url+f"token/{self.rest_account}/{self.rest_password}",
            params={
                "loginName": self.login_name,
            },
        )
