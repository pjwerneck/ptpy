

from compiler import misc, syntax, pycodegen, visitor
from compiler import symbols, pyassem, future

from compiler.consts import CO_NEWLOCALS

import ptpyparser
import ptpysymbols
import ptpybuiltins



class PtpyNameFinder(pycodegen.LocalNameFinder):
    def visitCode(self, node):
        self.names.add(node.name)


class PtpyNestedScopeMixin:
    """Defines initClass for nested scoping"""
    def initClass(self):
        self.__class__.NameFinder = PtpyNameFinder
        self.__class__.BlockGen = PtpyBlockGenerator


class PtpyCodeGenerator(pycodegen.CodeGenerator):

    """This is NOT a concrete implementation of the abstract
    CodeGenerator class. It just changes some methods on the way they
    are supposed to work with Ptpy"""

    def checkClass(self):
        """Verify that class is constructed correctly"""
        try:
            assert hasattr(self, 'graph')
            assert getattr(self, 'NameFinder')
            assert getattr(self, 'BlockGen')
        except AssertionError, msg:
            intro = "Bad class construction for %s" % self.__class__.__name__
            raise AssertionError, intro

    def parseSymbols(self, tree):
        s = ptpysymbols.PtpySymbolVisitor()
        visitor.walk(tree, s)
        return s.scopes

    def makeClosure(self, gen, args, frees):
        if frees:
            for name in frees:
                self.emit('LOAD_CLOSURE', name)
            self.emit('BUILD_TUPLE', len(frees))


    def visitCode(self, node):
        gen = self.BlockGen(node, self.scopes, self.get_module(), node.lazy)
        visitor.walk(node.code, gen)
        gen.finish()
        self.set_lineno(node)

        #self.emit('LOAD_CONST', node.name)

        frees = gen.scope.get_free_vars()
        #print node.name, 'free', frees
        gen.scope.DEBUG()
        self.makeClosure(gen, 0, frees)

        self.emit('LOAD_CONST', gen)
        
        if not node.lazy:
            if frees:
                self.emit('MAKE_CLOSURE', 0)
            else:
                self.emit('MAKE_FUNCTION', 0)
            #self.emit('CALL_FUNCTION', 0)

        self.storeName(node.name)

        if node.wrapper is not None:
            # load wrapper callable to TOS
            self.visit(node.wrapper)
            # load pattern name to TOS
            self.emit('LOAD_CONST', node.name)
            # load pattern to TOS
            self.loadName(node.name)
            # call wrapper(name, pattern)
            self.emit('CALL_FUNCTION', 2)
            # store it back
            self.storeName(node.name)



class PtpyAbstractBlockCode:
    optimized = 0
    def __init__(self, block, scopes, module):
        self.block_name = block.name
        self.module = module
        self.graph = pyassem.PyFlowGraph(block.name, block.filename,
                                           optimized=0)
        self.super_init()
        lnf = visitor.walk(block.code, self.NameFinder(), verbose=0)
        self.locals.push(lnf.getLocals())
        if not self.lazy:
            self.graph.setFlag(CO_NEWLOCALS)
        if block.doc:
            self.setDocstring(block.doc)

    def get_module(self):
        return self.module

    def finish(self):
        self.graph.startExitBlock()
        self.emit('LOAD_LOCALS')
        self.emit('RETURN_VALUE')


class PtpyBlockGenerator(PtpyNestedScopeMixin,
                         PtpyAbstractBlockCode,
                         PtpyCodeGenerator):
    super_init = PtpyCodeGenerator.__init__
    scopes = None

    __super_init = PtpyAbstractBlockCode.__init__

    def __init__(self, block, scopes, module, lazy=False):
        self.scopes = scopes
        self.scope = scopes[block]
        self.lazy = lazy
        self.__super_init(block, scopes, module)
        self.graph.setFreeVars(self.scope.get_free_vars())
        self.graph.setCellVars(self.scope.get_cell_vars())
        self.set_lineno(block)
        



class PtpyModuleCodeGenerator(PtpyNestedScopeMixin, PtpyCodeGenerator):
    __super_init = PtpyCodeGenerator.__init__

    scopes = None

    def __init__(self, tree):
        self.graph = pyassem.PyFlowGraph("<module>", tree.filename)
        self.futures = future.find_futures(tree)
        self.__super_init()
        visitor.walk(tree, self)

    def get_module(self):
        return self

        

class PtpyCompiler(object):
    def __init__(self):
        self.parser = ptpyparser.PtpyParser()

    def compile(self, code, filename="<string>"):
        tree = self.parser.parse(code)
        misc.set_filename(filename, tree)
        syntax.check(tree)
        gen = PtpyModuleCodeGenerator(tree)
        code = gen.getCode()
        return code



def main():
    import dis
    compiler = PtpyCompiler()
    code = compiler.compile(open("sample_ptpy.py").read())
    #dis.dis(code)
    gnamespace = {'a':1}
    gnamespace.update(ptpybuiltins.__dict__)

    namespace = {}

    exec code in gnamespace, namespace
    #del namespace['__builtins__']

    #print namespace
    dis.dis(namespace['m'])

if __name__ == '__main__':
    main()
