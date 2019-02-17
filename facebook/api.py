import requests
from urllib.parse import urlencode
from .exceptions import FacebookException


class API:
    _app_id = None
    _app_secret = None
    _access_token = None
    _auth = None
    _api_base_url = 'https://graph.facebook.com/v{version}/'
    _authorization_url = 'https://www.facebook.com/v{version}/dialog/oauth'
    _access_token_url = 'https://graph.facebook.com/v{version}/oauth/access_token'

    def __init__(self, app_id, app_secret, access_token=None, version=2.8):
        self._app_id = app_id
        self._app_secret = app_secret
        self._access_token = access_token
        self.set_version(version)

    def set_version(self, version):
        self._api_base_url = self._api_base_url.format(version=version)
        self._authorization_url = self._authorization_url.format(version=version)
        self._access_token_url = self._access_token_url.format(version=version)

    def get_authorization_url(self, callback, **kwargs):
        return self._authorization_url + '?' + urlencode({**{
            'client_id': self._app_id,
            'response_type': 'code',
            'redirect_uri': callback,
            'state': '9sdfhkj34897skdfh38497sksdf34dfdhfj',
            'scope': 'read_stream'
        }, **kwargs})

    def get_access_token(self, code, callback):
        response = requests.post(self._access_token_url, data={
            'client_id': self._app_id,
            'client_secret': self._app_secret,
            'redirect_uri': callback,
            'code': code
        })

        if response.status_code != 200:
            raise FacebookException(response.status_code, response.json())

        token = response.json()
        self.set_access_token(token['access_token'])
        return token

    def set_access_token(self, access_token):
        self._access_token = access_token

    def get(self, endpoint, **kwargs):
        return self.request('get', endpoint, params=kwargs)

    def post(self, endpoint, **kwargs):
        return self.request('post', endpoint, data=kwargs)

    def request(self, method, endpoint, **kwargs):
        authentication = {
            'access_token': self._access_token
        }

        if 'params' in kwargs:
            kwargs['params'] = {**kwargs['params'], **authentication}

        if 'data' in kwargs:
            kwargs['data'] = {**kwargs['data'], **authentication}

        url = self._api_base_url + endpoint if 'url' not in kwargs else kwargs['url']
        response = getattr(requests, method)(url, **kwargs)

        if response.status_code < 200 or response.status_code > 299:
            raise FacebookException(response.status_code, response.json())

        return response.json()
