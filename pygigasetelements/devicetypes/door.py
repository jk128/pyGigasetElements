from pygigasetelements import connection
from pygigasetelements.devicetypes.element import Element


class Door(Element):
    def __init__(self, base, id, **kwargs):
        self._base = base
        super(Door, self).__init__(id, **kwargs)

    def _retrieve(self):
        data = self.get(connection.URL_BASE)
        basedata = next((base for base in data if base['id'] == self._base._id))
        values = next((sensor for sensor in basedata['sensors'] if sensor['id'] == self._id))
        return values

    @property
    def position_status(self):
        self._update()
        return self._position_status
