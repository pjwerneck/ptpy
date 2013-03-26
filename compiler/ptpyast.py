
from compiler.ast import *


class Code(Node):
    def __init__(self, name, code, wrapper=None, lazy=True, lineno=None):
        self.name = name
        self.code = code
        self.wrapper = wrapper
        self.lineno = lineno
        self.doc = None
        self.lazy = lazy

    def getChildren(self):
        children = []
        children.append(self.name)
        if self.wrapper is not None:
            children.append(self.wrapper)
        children.append(self.code)
        return tuple(children)

    def getChildNodes(self):
        nodelist = []
        nodelist.append(self.code)
        return tuple(nodelist)
    

