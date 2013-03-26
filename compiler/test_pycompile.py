

"""
exec x


"""

from compiler import ast, misc, syntax, pycodegen
from compiler.consts import *
import compiler
import dis


def traverse_tree(node, level=0):
    if node is None:
        raise StopIteration
    tab = level*'    '

    yield node
    for subnode in node:
        if not isinstance(subnode, ast.Node):
            yield subnode
            continue
        for subiter in traverse_tree(subnode, level+1):
            yield subiter


def traverse(node, level=""):
    if node is None:
        raise StopIteration
    
    yield "%s%s"%(level, node.__class__.__name__)
    for subnode in node:
        if not isinstance(subnode, ast.Node):
            yield "%s%r"%(level+" ", subnode)
            continue
        for subiter in traverse(subnode, level+" "):
            yield "%s%s"%(level, subiter)


a = 1

def test_closure():
    import new

    _derefblock = new.code(0, 0, 1, 3, '\x88\x00\x00Sd\x00\x00S', (None,),
                           ('cell',), (), '', '', 2, '', ('cell',))

    def deref_cell(cell):
        return new.function(_derefblock, {}, "", (), (cell,))() 

    #a = 1
    def m():
        b = a + 2
        def n():
            c = b + 3
        #dis.dis(n)
        n()
    dis.dis(m)
    m()


test_closure()

