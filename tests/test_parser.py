# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Sat Sep 29 00:23:11 2012"


import unittest

from compiler import ast, misc, syntax, pycodegen
from compiler.consts import *

import ply.yacc as yacc

from ptpy.p_parser import PtpyParser
from ptpy.p_compiler import PtpyCompiler




class PtpyTestCompiler(object):
    def __init__(self):
        self.parser = PtpyParser()

    def compile(self, code, filename="<string>"):
        tree = self.parser.parse(code)
        misc.set_filename(filename, tree)
        syntax.check(tree)
        gen = pycodegen.ModuleCodeGenerator(tree)
        code = gen.getCode()
        return code


class BaseTest(unittest.TestCase):
    def get_string(self, method):
        # this will get the docstring from a method, strip the first 2
        # lines and then cut first 8 characters
        data = method.__doc__
        lines = data.split('\n')[2:]
        lines = "\n".join(line[8:] for line in lines)
        return lines

    def get_lines(self, method):
        data = self.get_string(method)
        for line in data.split('\n'):
            yield line

    def flatten_tree(self, tree):
        stack = []
        for level, type, value in tree:
            if isinstance(value, str):
                stack.append(value)
        return stack
            
    def parse_expr(self, expr):
        parser = ptpyparser.PtpyParser()
        result = ptpyparser.traverse(parser.parse(expr))
        return self.flatten_tree(result)


def traverse_tree(node):
    if node is None:
        raise StopIteration
    
    yield node
    for subnode in node:
        if not isinstance(subnode, ast.Node):
            yield subnode
            continue
        for subiter in traverse_tree(subnode):
            yield subiter


class TestParserRules(BaseTest):
    def setUp(self):
        self.parser = PtpyParser()

    def do_test_header(self, tree):
        assert isinstance(tree.next(), ast.Module)
        assert tree.next() is None # FIXME: why None here?
        assert isinstance(tree.next(), ast.Stmt)

    def test_multiple_item_tuple(self):
        """Test tuple with multiple items

        (a, b, c)
        
        #
        """
        code = self.get_string(self.test_multiple_item_tuple)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Tuple)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'c'
        self.assertRaises(StopIteration, tree.next)
        
    def test_single_item_tuple(self):
        """Test single item tuple with trailing comma

        (a,)
        
        """
        code = self.get_string(self.test_single_item_tuple)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Tuple)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        self.assertRaises(StopIteration, tree.next)
        

    def test_booleans(self):
        """Test all boolean operators

        not a
        a and b
        a or b
        """
        code = self.get_string(self.test_booleans)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Not)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
            
        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.And)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
            
        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Or)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        self.assertRaises(StopIteration, tree.next)

            
    def test_all_comparisons(self):
        """Test all comparisons

        a < b
        a <= b
        a > b
        a >= b
        a != b
        a == b
        a is b
        a is not b
        a in b
        a not in b

        """

        code = self.get_string(self.test_all_comparisons)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)

        for op in ('<', '<=', '>', '>=', '!=', '==', 'is',
                   'is not', 'in', 'not in'):
            assert isinstance(tree.next(), ast.Discard), op
            assert isinstance(tree.next(), ast.Compare), op
            assert isinstance(tree.next(), ast.Name), op
            assert tree.next() == 'a', op
            assert tree.next() == op, op
            assert isinstance(tree.next(), ast.Name), op
            assert tree.next() == 'b', op
        self.assertRaises(StopIteration, tree.next)


    def test_all_exprs(self):
        """Test all expressions

        a ** b
        -a
        +a
        a * b
        a / b
        a % b
        a + b
        a - b
        a << b
        a >> b
        a & b
        a ^ b
        a | b

        """
        code = self.get_string(self.test_all_exprs)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Power)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        
        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.UnarySub)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        
        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.UnaryAdd)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Mul)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        
        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Div)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        
        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Mod)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        
        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Add)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        
        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Sub)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        
        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.LeftShift)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        
        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.RightShift)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        
        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Bitand)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Bitxor)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Bitor)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'

        self.assertRaises(StopIteration, tree.next)


    def test_augmented_assignments(self):
        """Test augmented assignments

        a += b
        a -= b
        a /= b
        a *= b
        a %= b
        a **= b
        a <<= b
        a >>= b
        a &= b
        a |= b
        a ^= b
        
        """
        code = self.get_string(self.test_augmented_assignments)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)

        assert isinstance(tree.next(), ast.AugAssign)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == '+='
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        
        assert isinstance(tree.next(), ast.AugAssign)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == '-='
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        
        assert isinstance(tree.next(), ast.AugAssign)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == '/='
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'

        assert isinstance(tree.next(), ast.AugAssign)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == '*='
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        
        assert isinstance(tree.next(), ast.AugAssign)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == '%='
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'

        assert isinstance(tree.next(), ast.AugAssign)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == '**='
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'

        assert isinstance(tree.next(), ast.AugAssign)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == '<<='
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'

        assert isinstance(tree.next(), ast.AugAssign)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == '>>='
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'

        assert isinstance(tree.next(), ast.AugAssign)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == '&='
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'

        assert isinstance(tree.next(), ast.AugAssign)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == '|='
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'

        assert isinstance(tree.next(), ast.AugAssign)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == '^='
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'


    def test_trailed_atom(self):
        """Test the base atoms with a function call

        a(x, y, z)
        
        """
        code = self.get_string(self.test_trailed_atom)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.CallFunc)

        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'x'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'y'
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'z'

        assert tree.next() is None
        assert tree.next() is None
        
        self.assertRaises(StopIteration, tree.next)
        

    def test_base_atoms(self):
        '''Test the base atoms

        a
        1
        3.14
        "hello"

        '''
        code = self.get_string(self.test_base_atoms)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Const)
        assert tree.next() == 1

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Const)
        assert tree.next() == 3.14

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Const)
        assert tree.next() == "hello"

        self.assertRaises(StopIteration, tree.next)
        
    def test_assignment(self):
        """Test assignment

        x = a
        y = b

        """
        code = self.get_string(self.test_assignment)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)
        
        assert isinstance(tree.next(), ast.Assign)
        assert isinstance(tree.next(), ast.AssName)
        assert tree.next() == 'x'
        assert tree.next() == OP_ASSIGN
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'

        assert isinstance(tree.next(), ast.Assign)
        assert isinstance(tree.next(), ast.AssName)
        assert tree.next() == 'y'
        assert tree.next() == OP_ASSIGN
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        self.assertRaises(StopIteration, tree.next)

    def test_comments_are_ignored(self):
        """Test comments are ignored by tokenizer

        # this is another comment
        x = a
        y = b

        """
        # FIXME: comments at the end of input raise an error (an extra
        # ENDMARKER?)
        code = self.get_string(self.test_comments_are_ignored)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)
        
        assert isinstance(tree.next(), ast.Assign)
        assert isinstance(tree.next(), ast.AssName)
        assert tree.next() == 'x'
        assert tree.next() == OP_ASSIGN
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'

        assert isinstance(tree.next(), ast.Assign)
        assert isinstance(tree.next(), ast.AssName)
        assert tree.next() == 'y'
        assert tree.next() == OP_ASSIGN
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'b'
        self.assertRaises(StopIteration, tree.next)

    def test_get_attribute(self):
        """Test get attribute

        a.x
        
        """
        code = self.get_string(self.test_get_attribute)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)

        assert isinstance(tree.next(), ast.Discard)
        assert isinstance(tree.next(), ast.Getattr)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'a'
        assert tree.next() == 'x'
        self.assertRaises(StopIteration, tree.next)
        
    def test_attribute_assignment(self):
        """Test attribute assignment

        o.a = v

        """
        code = self.get_string(self.test_attribute_assignment)
        tree = traverse_tree(self.parser.parse(code))
        self.do_test_header(tree)
        
        assert isinstance(tree.next(), ast.Assign)
        assert isinstance(tree.next(), ast.AssAttr)
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'o'
        assert tree.next() == 'a'
        assert tree.next() == OP_ASSIGN
        assert isinstance(tree.next(), ast.Name)
        assert tree.next() == 'v'
        self.assertRaises(StopIteration, tree.next)

    def test_atoms_with_no_comma_fail(self):
        """Test if the expressions below fail

        1 2 3
        a b c
        """
        code = self.get_string(self.test_atoms_with_no_comma_fail)
        self.assertRaises(SyntaxError, self.parser.parse, code)

    def test_assignment_to_literal_fails(self):
        """Test if an assignment to literal fails

        1 = 0
        
        """
        code = self.get_string(self.test_assignment_to_literal_fails)
        print self.parser._lexer
        #self.assertRaises(SyntaxError, self.parser.parse, code)






if __name__ == '__main__':
    unittest.main()
