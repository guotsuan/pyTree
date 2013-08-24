import uuid


class Node(object):

    (ADD, DELETE, INSERT) = range(3)


    def __init__(self, tag=None, identifier=None, expanded=True):
        self.tag = tag
        self._identifier = self.set_identifier(identifier)
        self.expanded = expanded
        self._bpointer = None
        self._fpointer = []
        self.pos_x = None
        self.pos_y = None
        self.width = 1  # Max. width (in the plotting sense) of subtree
        self.height = None  # Number of tree levels below (incl. self)
        self.depth = None  # Number of tree levels above (excl. self)


    @classmethod
    def sanitize_id(cls, identifier):
        return str(identifier).strip().replace(" ", "_")


    def set_identifier(self, identifier):
        if identifier is None:
            return str(uuid.uuid1())
        else:
            return self.sanitize_id(identifier)


    @property
    def identifier(self):
        return self._identifier


    @property
    def bpointer(self):
        return self._bpointer


    @bpointer.setter
    def bpointer(self, value):
        if value is not None:
            self._bpointer = self.sanitize_id(value)


    @property
    def fpointer(self):
        return self._fpointer


    @fpointer.setter
    def fpointer(self, value):
        if value is not None and isinstance(value, list):
            self._fpointer = value


    def update_fpointer(self, identifier, mode=ADD):
        if mode is self.ADD:
            self._fpointer.append(self.sanitize_id(identifier))
        elif mode is self.DELETE:
            self._fpointer.remove(self.sanitize_id(identifier))
        elif mode is self.INSERT:
            self._fpointer = [self.sanitize_id(identifier)]
