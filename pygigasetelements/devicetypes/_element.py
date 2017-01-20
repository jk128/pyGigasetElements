from pygigasetelements.connection import ElementsConnection, _URL_BASE
from .base import Base


class Element(object):
    def __init__(self, id, **kwargs):
        self._id = id

    def get(self, url):
        """
        Wrapper for making a GET request
        :param url: URL which should be requested
        :return: parsed response
        """
        f = ElementsConnection()
        return f.get(url)

    def post(self, url, payload):
        """
        Wrapper for making a POST request
        :param url: URL which should be requested
        :return: parsed response
        """
        f = ElementsConnection()
        return f.post(url, payload)

    def _update(self):
        """
        Function which retrieves new data and updates the calling object accordingly
        """
        data = self.get(_URL_BASE)

        if isinstance(self, Base):
            values = next((base for base in data if base['id'] == self._id))
        else:
            basedata = next((base for base in data if base['id'] == self._base._id))
            values = next((sensor for sensor in basedata['sensors'] if sensor['id'] == self._id))

        for key, value in values.items():
            setattr(self, '_' + key, value)

    @property
    def friendly_name(self):
        self._update()
        return getattr(self, '_friendly_name', None)

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.friendly_name
