


import ply.yacc as yacc
import unittest
from compiler import ast

from compiler import misc, syntax, pycodegen
from compiler.consts import *

from test_ptpyparser import BaseTest

from ptpyparser import PtpyParser
from ptpycompiler import PtpyCompiler

import ptpybuiltins



class TestCompiledCode(BaseTest):
    def setUp(self):
        self.compiler = PtpyCompiler()

    def run_code(self, code, namespace):
        bcode = self.compiler.compile(code)
        ptpyglobals = {}
        ptpyglobals.update(ptpybuiltins.__dict__)
        exec bcode in ptpyglobals, namespace

    def test_single_assignment(self):
        """Test a single assignment

        a = 1
        """
        code = self.get_string(self.test_single_assignment)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace, {'a': 1})

    def test_comments_are_ignored(self):
        """Test comments are ignored by parser/compiler

        # this is a comment
        a = 1

        """
        code = self.get_string(self.test_comments_are_ignored)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace, {'a': 1})

    def test_assign_expr(self):
        """Test a few assignment expressions
        
        a = 1 + 2 * 3
        b = (1 + 2) * 3
        c = b % a
        d = 2 ** 6
        pi = 3.14
        s = "Hello World!"
        
        """
        code = self.get_string(self.test_assign_expr)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace, {'a': 7,
                                     'b': 9,
                                     'c': 2,
                                     'd': 64,
                                     'pi': 3.14,
                                     # FIXME: strip quotes out of strings
                                     's': "Hello World!",
                                     }
                         )

    def test_list_literal(self):
        """Test if the list literal works

        x = [1, 2, 3]
        """
        code = self.get_string(self.test_list_literal)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace, {'x':[1, 2, 3]})

    def test_tuple_literal(self):
        """Test if the tuple literal works

        x = (1, 2, 3)
        """
        code = self.get_string(self.test_tuple_literal)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace, {'x':(1, 2, 3)})

    def test_dict_literal(self):
        """Test if the dict literal works

        x = {"a":1, "b":2, "c":(3, 4, 5)}
        """
        code = self.get_string(self.test_dict_literal)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace, {'x':{'a':1, 'b':2, 'c':(3, 4, 5)}})

    def test_string_literal(self):
        """Test if the string literal works

        x = "abc"
        """
        code = self.get_string(self.test_string_literal)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace, {'x':"abc"})
    
    def test_if_stmt(self):
        """Test the if statement

        a = 1
        if a == 1:
            b = 1

        """
        code = self.get_string(self.test_if_stmt)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace, {'a': 1, 'b': 1})

    def test_assert_stmt(self):
        """Test the assert statement

        a = 1
        assert a == 1

        """
        code = self.get_string(self.test_assert_stmt)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace, {'a': 1})

    def test_assert_stmt_fails(self):
        # FIXME!
        """Test if the assert statement fails

        a = 0
        assert a == 1
        c = a == 1

        """
        code = self.get_string(self.test_assert_stmt_fails)
        namespace = {}
        self.assertRaises(AssertionError, self.run_code, code, namespace)

    def test_assign_to_literal_fails(self):
        """Test if an assignment to literal fails

        1 = 0

        """
        code = self.get_string(self.test_assign_to_literal_fails)
        namespace = {}
        self.assertRaises(SyntaxError, self.run_code, code, namespace)

    def test_single_conditional(self):
        """Test if an 'if' conditional works

        if x:
            y = 1
        """
        code = self.get_string(self.test_single_conditional)
        namespace = {'x':1, 'y':0}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['x'], 1)
        self.assertEqual(namespace['y'], 1)

        namespace = {'x':0, 'y':1}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['x'], 0)
        self.assertEqual(namespace['y'], 1)

    def test_multiple_conditional(self):
        """Test if a multiple 'if' conditional works

        if x > 0:
            y = 1
        elif x < 0:
            y = 2
        elif x == 0:
            y = 3
            
        """
        code = self.get_string(self.test_multiple_conditional)
        namespace = {'x':1}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['x'], 1)
        self.assertEqual(namespace['y'], 1)

        namespace = {'x':0}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['x'], 0)
        self.assertEqual(namespace['y'], 3)
        
        namespace = {'x':-1}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['x'], -1)
        self.assertEqual(namespace['y'], 2)
        
    def test_if_elif_else_statement(self):
        """Test if/elif/else statement

        if x > 0:
            y = 1
        elif x < 0:
            y = 2
        else:
            y = 3
            
        """
        code = self.get_string(self.test_if_elif_else_statement)
        namespace = {'x':1}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['x'], 1)
        self.assertEqual(namespace['y'], 1)

        namespace = {'x':0}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['x'], 0)
        self.assertEqual(namespace['y'], 3)
        
        namespace = {'x':-1}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['x'], -1)
        self.assertEqual(namespace['y'], 2)
        
    def test_if_else_statement(self):
        """Test if/else statement

        if x > 0:
            y = 1
        else:
            y = 2
            
        """
        code = self.get_string(self.test_if_else_statement)
        namespace = {'x':1}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['x'], 1)
        self.assertEqual(namespace['y'], 1)

        namespace = {'x':0}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['x'], 0)
        self.assertEqual(namespace['y'], 2)

        
    def test_elif_before_if_fails(self):
        """Test if putting elif before if fails

        elif x > 0:
            y = 1
        if x < 0:
            y = 2
            
        """
        code = self.get_string(self.test_elif_before_if_fails)
        namespace = {}
        self.assertRaises(SyntaxError, self.run_code, code, namespace)

        
    def test_for_loop(self):
        """Test for loop

        for x in seq:
            v = v + x
            
        """
        code = self.get_string(self.test_for_loop)
        namespace = {'v':0, 'seq':[1, 2, 3, 4, 5]}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['v'], 15)

    def test_for_else_loop(self):
        """Test for/else loop

        for x in seq:
            if x == 2:
                continue
            v = v + x
            if v > 10:
                break
        else:
            v = -1
            
        """
        code = self.get_string(self.test_for_else_loop)
        namespace = {'v':0, 'seq':[1, 2, 3, 4, 5]}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['v'], 13)

        code = self.get_string(self.test_for_else_loop)
        namespace = {'v':0, 'seq':[3, 3, 3, 3]}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['v'], 12)

        code = self.get_string(self.test_for_else_loop)
        namespace = {'v':0, 'seq':[1, 2, 3, 4]}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['v'], -1)

        
    def test_while_loop(self):
        """Test while loop
        
        while v < 10:
            v += 1
            
        """
        code = self.get_string(self.test_while_loop)
        namespace = {'v':0}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['v'], 10)

    def test_while_else_loop(self):
        """Test while/else loop
        
        while v < 10:
            v += 1
        else:
            v = -1
            
        """
        code = self.get_string(self.test_while_else_loop)
        namespace = {'v':0}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['v'], -1)

        
    def test_getattribute(self):
        """Test if getting an attribute works

        a = x.real
        b = x.imag
        
        """
        code = self.get_string(self.test_getattribute)
        namespace = {'x':complex(1, 2)}
        self.run_code(code, namespace)        
        self.assertEqual(namespace['x'], complex(1, 2))
        self.assertEqual(namespace['a'], 1.0)
        self.assertEqual(namespace['b'], 2.0)

    def test_setattribute(self):
        """Test if setting an attribute works

        o.a = 0
        o.b = 1
        o.c = "hello!"

        """
        class TestObject(object):
            pass
        o = TestObject()

        code = self.get_string(self.test_setattribute)
        namespace = {'o':o}
        self.run_code(code, namespace)        

        self.assertEqual(o.a, 0)
        self.assertEqual(o.b, 1)
        self.assertEqual(o.c, "hello!")
        
    def test_single_let(self):
        """Test single let 

        let n:
            a = 1
            b = 2
            c = a + b
            d = [a, b, c]
        
        """
        code = self.get_string(self.test_single_let)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace['n'], {'a':1, 'b':2, 'c':3, 'd':[1, 2, 3]})

    def test_multiple_let(self):
        """Test if multiple let don't mess each other

        let m:
            a = 1
            b = 2

        let n:
            a = 3
            b = 4

        """
        code = self.get_string(self.test_multiple_let)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace['m'], {'a':1, 'b':2})
        self.assertEqual(namespace['n'], {'a':3, 'b':4})
        
    def test_nested_let(self):
        """Test if nested let don't mess each other

        let m:
            a = 1

            let n:
                a = 2

        """
        code = self.get_string(self.test_nested_let)
        namespace = {}
        self.run_code(code, namespace)
        self.assertEqual(namespace['m'], {'a':1, 'n':{'a':2}})

    def test_multiple_nested_let(self):
        """Test if multiple nested let work

        let m:
            a = 1

            let n:
                b = 2

                let o:
                    c = 3

        """
        code = self.get_string(self.test_multiple_nested_let)
        namespace = {}
        self.run_code(code, namespace)
        
        self.assertEqual(namespace['m'], {'a':1, 'n':{'b':2, 'o':{'c':3}}})

    def test_define(self):
        """Test define 

        define m:
            a = 1
            b = 2
            
        """
        code = self.get_string(self.test_define)
        namespace = {}
        self.run_code(code, namespace)
        m = {}
        exec namespace['m'] in globals(), m
        self.assertEqual(m, {'a':1, 'b':2})

    def test_multiple_define(self):
        """Test if multiple define work

        define m:
            a = 1
            b = 2

        define n:
            a = 3
            b = 4
            
        """
        code = self.get_string(self.test_multiple_define)
        namespace = {}
        self.run_code(code, namespace)
        m = {}
        n = {}
        exec namespace['m'] in globals(), m
        exec namespace['n'] in globals(), n
        
        self.assertEqual(m, {'a':1, 'b':2})
        self.assertEqual(n, {'a':3, 'b':4})

    def test_nested_define(self):
        """Test if nested define work

        define m:
            a = 1
            b = 2

            define n:
                a = 3
                b = 4

        """
        code = self.get_string(self.test_nested_define)
        namespace = {}
        self.run_code(code, namespace)
        m = {}
        n = {}
        exec namespace['m'] in globals(), m
        exec m['n'] in globals(), n
        m['n'] = n
        
        self.assertEqual(m, {'a':1, 'b':2, 'n':{'a':3, 'b':4}})

    def test_let_closures(self):
        """Test if let closures resolve properly 

        a = 1
        let m:
            b = 2
            let n:
                c = 3
                let o:
                    d = a + b + c

        """
        code = self.get_string(self.test_let_closures)
        namespace = {}
        self.run_code(code, namespace)

    def test_let_with_wrapper(self):
        """Test let statement with namespace wrapper

        let namespace m:
            a = 1
            b = 2
            c = "3"
            d = [1, 2, 3, 4]
            """
        code = self.get_string(self.test_let_with_wrapper)
        namespace = {}
        self.run_code(code, namespace)

        m = namespace['m']
        self.assertEqual(type(m), ptpybuiltins.namespace)
        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 2)
        self.assertEqual(m.c, "3")
        self.assertEqual(m.d, [1, 2, 3, 4])
       
    def test_define_with_wrapper(self):
        """Test define statement with function wrapper

        define function f:
            a = 1
            b = 2
            c = "3"
            d = [1, 2, 3, 4]

        """
        code = self.get_string(self.test_define_with_wrapper)
        namespace = {}
        self.run_code(code, namespace)

        f = namespace['f']
        self.assertEqual(type(f), ptpybuiltins.function)
        self.assertEqual(f.__name__, 'f')
        #self.assertEqual(f.__code__, None)

        #c = f.__code__
        #for n in dir(c):
        #    print n, getattr(c, n)
        
    


if __name__ == '__main__':
    unittest.main()
