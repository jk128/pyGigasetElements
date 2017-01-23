from pygigasetelements.devicetypes.element import Element


class Door(Element):
    def __init__(self, base, id, **kwargs):
        self._base = base
        super(Door, self).__init__(id, **kwargs)

    @property
    def position_status(self):
        self._update()
        return self._position_status
