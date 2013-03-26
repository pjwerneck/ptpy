# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Sat Sep 29 00:23:11 2012"


from compiler import misc, syntax, pycodegen, visitor, symbols

from compiler.consts import *


class CodeScope(symbols.Scope):

    def check_name(self, name):
        if self.globals.has_key(name):
            return SC_GLOBAL
        if self.cells.has_key(name):
            return SC_CELL
        if self.defs.has_key(name):
            return SC_LOCAL
        if self.nested and (self.frees.has_key(name) or
                            self.uses.has_key(name)):
            return SC_FREE
        if self.nested:
            return SC_UNKNOWN
        else:
            return SC_GLOBAL

    def add_frees(self, names):
        child_globals = []
        for name in names:
            sc = self.check_name(name)
            if self.nested:
                if sc == SC_UNKNOWN or sc == SC_FREE:# or isinstance(self, CodeScope):
                    self.frees[name] = 1
                elif sc == SC_GLOBAL:
                    child_globals.append(name)
                #elif isinstance(self, CodeScope) and sc == SC_LOCAL:
                #    self.cells[name] = 1
                elif sc != SC_CELL:
                    child_globals.append(name)
            else:
                if sc == SC_LOCAL:
                    self.cells[name] = 1
                elif sc != SC_CELL:
                    child_globals.append(name)

        
        return child_globals
        


#    __super_init = symbols.Scope.__init__
#
#    def __init__(self, name, module):
#        self.__super_init(name, module)


class PtpySymbolVisitor(symbols.SymbolVisitor):
    def visitCode(self, node, parent):
        parent.add_def(node.name)
        scope = CodeScope(node.name, self.module)
        #if parent.nested or isinstance(parent, symbols.FunctionScope):
        if parent.nested or isinstance(parent, CodeScope):
            scope.nested = 1
        #if node.doc is not None:
        #    scope.add_def('__doc__')
        #scope.add_def('__module__')
        self.scopes[node] = scope

        #prev = self.klass
        #self.klass = node.name
        self.visit(node.code, scope)
        #self.klass = prev
        self.handle_free_vars(scope, parent)
        
