"""
This API provides access to the Gigaset Elements Family
This package can be used with Python3 applications
coding=utf-8
"""

import time

import requests

from pygigasetelements.devicetypes.base import Base
from pygigasetelements.devicetypes.door import Door

_EMAIL = ""  # Your Email-login for https://my.gigaset-elements.com
_PASSWORD = ""  # Your account password

_URL_IDENTITY = 'https://im.gigaset-elements.de/identity/api/v1/user/login'
_URL_AUTH = 'https://api.gigaset-elements.de/api/v1/auth/openid/begin?op=gigaset'
_URL_EVENTS = 'https://api.gigaset-elements.de/api/v2/me/events'
_URL_BASE = 'https://api.gigaset-elements.de/api/v1/me/basestations'
_URL_CAMERA = 'https://api.gigaset-elements.de/api/v1/me/cameras'
_URL_HEALTH = 'https://api.gigaset-elements.de/api/v2/me/health'
_URL_CHANNEL = 'https://api.gigaset-elements.de/api/v1/me/notifications/users/channels'

AUTH_EXPIRE = 21540


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ElementsConnection(object, metaclass=Singleton):
    """
    Request authentication and keep cookietoken available through token method. Renew it automatically if necessary

    Args:
        email: Your Email-login for https://my.gigaset-elements.com
        password: Your account password
    """

    def __init__(self, email=_EMAIL, password=_PASSWORD):
        self.s = requests.session()
        self._login(email, password)

    def _login(self, email, password):
        payload = {'email': email,
                   'password': password}

        r = self._post(_URL_IDENTITY, payload)
        if not r['http'] == requests.codes.ok:
            raise Exception(r.get('message'))
        self._refreshToken()

    def _refreshToken(self):
        self._get(_URL_AUTH)
        self.expiration = time.time() + AUTH_EXPIRE

    def get(self, url):
        if self.expiration < time.time():  # Token should be renewed
            self._refreshToken()

        return self._get(url)

    def post(self, url, payload):
        if self.expiration < time.time():  # Token should be renewed
            self._refreshToken()

        return self._post(url, payload)

    def _discover(self):
        devices = list()
        r = self.get(_URL_BASE)

        for base in r:
            root = Base(id=base.get('id'))
            devices.append(root)

            for sensor in base['sensors']:
                if any(x in sensor['type'] for x in ['ds01', 'ds02']):
                    child = Door(base=root, id=sensor.get('id'))
                    devices.append(child)

        return devices

    @property
    def devices(self):
        return self._discover()

    def _get(self, url, head=False, seconds=90, end=1):
        """REST interaction using GET."""
        try:
            if head:
                header = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
                r = self.s.head(url, timeout=seconds, headers=header, allow_redirects=True)
            else:
                r = self.s.get(url, timeout=seconds, stream=False)
        except requests.exceptions.RequestException as e:
            print('HTTP ERROR' + ' | ' + str(e.message))
        if r.status_code != requests.codes.ok:
            print('HTTP ERROR' + ' | ' + str(r.status_code))
        try:
            data = r.json()
        except ValueError:
            data = r.text
        return data

    def _post(self, url, payload, head=None):
        """REST interaction using POST."""
        s = requests.Session()
        try:
            if head is not None:
                r = self.s.post(url, data=payload, timeout=90, stream=False, headers=head)
            else:
                r = self.s.post(url, data=payload, timeout=90, stream=False)
        except requests.exceptions.RequestException as e:
            print('HTTP ERROR' + ' | ' + str(e.message))
        if r.status_code != requests.codes.ok:
            print('HTTP ERROR' + ' | ' + str(r.status_code))
        try:
            commit_data = r.json()
        except ValueError:
            commit_data = r.text

        return commit_data
