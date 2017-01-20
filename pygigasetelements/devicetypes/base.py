import json

from pygigasetelements.connection import _URL_BASE
from ._element import Element


class Base(Element):
    __MODES = ['home', 'away', 'custom']

    def __init__(self, id, **kwargs):
        super(Base, self).__init__(id, **kwargs)

    @property
    def mode(self):
        """
        returns the current mode of Base

        :return: str home, away or custom
        """
        self._update()
        return self._intrusion_settings['active_mode']

    @mode.setter
    def mode(self, mode):
        """
        Sets alarm Mode on Base Station

        :param mode: 0 -> Home, 1 -> Away, 2-> Custom
        :return: Boolean
        """
        r = self.post(_URL_BASE + '/' + self._id,
                      json.dumps({'intrusion_settings': {'active_mode': self.__MODES[mode]}}))
