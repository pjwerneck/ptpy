



class namespace(object):
    def __init__(self, name, body):
        self.__body__ = body
        self.__parent__ = None

    def __getattr__(self, name):
        return self.__body__[name]


class function(object):
    def __init__(self, name, code):
        self.__name__ = name
        self.__code__ = code

    
