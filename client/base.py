# -*- coding: utf-8 -*-
import json
import time
import inspect
import logging

import requests


from ..session.memorystorage import MemoryStorage
from ..exceptions import OAClientException
from ..constants import OAErrorCode
from ..client.api.base import BaseOAAPI


logger = logging.getLogger(__name__)


def _is_api_endpoint(obj):
    return isinstance(obj, BaseOAAPI)


class BaseOAClient:

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, api_base_url, rest_account, rest_password, login_name, token=None, session=None, timeout=None, auto_retry=True):
        self.api_base_url = api_base_url
        self._http = requests.Session()
        self.rest_account = rest_account
        self.rest_password = rest_password
        self.login_name = login_name
        self.session = session or MemoryStorage()
        self.timeout = timeout
        self.auto_retry = auto_retry
        if token:
            self.session.set(self.token_key, token)

    @property
    def token_key(self):
        return f"{self.rest_account}_{self.login_name}_token"

    @property
    def binding_user_key(self):
        return f"{self.rest_account}_{self.login_name}_binding_user"


    def _request(self, method, url_or_endpoint, **kwargs):
        headers = {'Content-Type': 'application/json'}
        if not url_or_endpoint.startswith(("http://", "https://")):
            api_base_url = kwargs.pop("api_base_url", self.api_base_url)
            url = f"{api_base_url}{url_or_endpoint}"
        else:
            url = url_or_endpoint

        if "params" not in kwargs:
            kwargs["params"] = {}
        if isinstance(kwargs["params"], dict) and "token" not in kwargs["params"]:
            kwargs["params"]["token"] = self.token
        if isinstance(kwargs.get("data", ""), dict):
            
            body = json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode("utf-8")
            kwargs["data"] = body
        if "files" in kwargs:
            headers = {}
        kwargs["timeout"] = kwargs.get("timeout", self.timeout)
        result_processor = kwargs.pop("result_processor", None)
        res = self._http.request(method=method, headers=headers, url=url, **kwargs)
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise OAClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response,
            )

        return self._handle_result(res, method, url, result_processor, **kwargs)

    def _decode_result(self, res):
        try:
            result = json.loads(res.content.decode("utf-8", "ignore"), strict=False)
        except (TypeError, ValueError):
            # Return origin response object if we can not decode it as JSON
            logger.debug("Can not decode response as JSON", exc_info=True)
            return res
        return result

    def _handle_result(self, res, method=None, url=None, result_processor=None, **kwargs):
        if not isinstance(res, dict):
            result = self._decode_result(res)
        else:
            result = res

        if not isinstance(result, dict):
            return result

        if "code" in result and result["code"] != '0' and result["code"] != 0:
            code = int(result["code"])
            message = result.get("message", code)
            if self.auto_retry and code in (
                OAErrorCode.INVALID_ACCESS_TOKEN.value,
            ):
                logger.info("token expired, fetch a new one and retry request")
                self.fetch_token()
                token = self.session.get(self.token_key)
                kwargs["params"]["token"] = token
                return self._request(method=method, url_or_endpoint=url, result_processor=result_processor, **kwargs)
            else:
                raise OAClientException(code, message, client=self, request=res.request, response=res)

        return result if not result_processor else result_processor(result)

    def get(self, url, **kwargs):
        return self._request(method="get", url_or_endpoint=url, **kwargs)

    def post(self, url, **kwargs):
        return self._request(method="post", url_or_endpoint=url, **kwargs)

    def _fetch_token(self, url, params):
        """The real fetch token"""
        logger.info("Fetching token")
        res = self._http.get(url=url, params=params)
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise OAClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response,
            )
        result = res.json()
        if "code" in result and result["code"] != 0:
            raise OAClientException(
                result["code"],
                result["message"],
                client=self,
                request=res.request,
                response=res,
            )
        if "bindingUser" in result:
            self.session.set(self.binding_user_key, result["bindingUser"])

        self.session.set(self.token_key, result["id"])
        return result

    def fetch_token(self):
        raise NotImplementedError()

    @property
    def token(self):
        token = self.session.get(self.token_key)
        if token:
            return token
        self.fetch_token()
        return self.session.get(self.token_key)

    @property
    def binding_user(self):
        binding_user = self.session.get(self.binding_user_key)
        if binding_user:
           return  binding_user
        self.fetch_token()
        return self.session.get(self.binding_user_key)

