class LastPassUser(object)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.fullname = kwargs.get('fullname')
        self.groups = kwargs.get('groups')
        self.attribs = kwargs.get('attribs')
