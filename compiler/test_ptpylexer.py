# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Sat Sep 29 00:23:11 2012"




import ply.lex as lex
import ptpylexer
import unittest


class TestTokens(unittest.TestCase):
    def setUp(self):
        self.lexer = ptpylexer.PtpyLexer()

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


    def test_literals(self):
        '''Test literals, integers, float, strings, identifiers

        1
        145
        1.3
        3.145
        "hi mom!"
        variable
        '''
        lines = self.get_lines(self.test_literals)

        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST')
        self.assertEqual(tok.value, '1')

        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST')
        self.assertEqual(tok.value, '145')

        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'FCONST')
        self.assertEqual(tok.value, '1.3')

        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'FCONST')
        self.assertEqual(tok.value, '3.145')

        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'SCONST')
        self.assertEqual(tok.value, "hi mom!", tok.value)

        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME')
        self.assertEqual(tok.value, 'variable', tok.value)


    def test_operators(self):
        """Test operators

        a = 1 + 2
        b = 41 - 1
        c = 5 * 96
        d = 40.4 / 4
        e = 9 % 2
        """
        lines = self.get_lines(self.test_operators)

        # a = 1 + 2
        tokens = [('NAME', 'a'),
                  ('ASSIGN', '='),
                  ('ICONST', '1'),
                  ('PLUS', '+'),
                  ('ICONST', '2')]

        self.lexer.input(lines.next())
        for tok, (t, v) in zip(self.lexer, tokens):
            self.assertEqual(tok.type, t)
            self.assertEqual(tok.value, v)

        # b = 41 - 1
        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'b')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ASSIGN')
        self.assertEqual(tok.value, '=')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST')
        self.assertEqual(tok.value, '41')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'MINUS')
        self.assertEqual(tok.value, '-')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST')
        self.assertEqual(tok.value, '1')

        # c = 5 * 96
        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'c')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ASSIGN')
        self.assertEqual(tok.value, '=')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST')
        self.assertEqual(tok.value, '5')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'MULT')
        self.assertEqual(tok.value, '*')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST')
        self.assertEqual(tok.value, '96')

        # d = 40.4 / 4
        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'd')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ASSIGN')
        self.assertEqual(tok.value, '=')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'FCONST')
        self.assertEqual(tok.value, '40.4')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'DIV')
        self.assertEqual(tok.value, '/')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST')
        self.assertEqual(tok.value, '4')

        # e = 9 % 2
        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'e')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ASSIGN')
        self.assertEqual(tok.value, '=')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST')
        self.assertEqual(tok.value, '9')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'MOD')
        self.assertEqual(tok.value, '%')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST')
        self.assertEqual(tok.value, '2')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')

        assert self.lexer.token().type == 'ENDMARKER'
        assert self.lexer.token() is None


    def test_brackets(self):
        """Test brackets

        [1, 2, 3]
        """
        lines = self.get_lines(self.test_brackets)

        # [1, 2, 3]
        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'LBRACKET', tok.type)
        self.assertEqual(tok.value, '[')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '1')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COMMA', tok.type)
        self.assertEqual(tok.value, ',')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '2')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COMMA', tok.type)
        self.assertEqual(tok.value, ',')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '3')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'RBRACKET', tok.type)
        self.assertEqual(tok.value, ']')

    def test_braces(self):
        """Test braces for dict

        {a:1, b:2, c:3}

        """
        lines = self.get_lines(self.test_braces)

        # {a:1, b:2, c:3}
        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'LBRACE', tok.type)
        self.assertEqual(tok.value, '{')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'a')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COLON', tok.type)
        self.assertEqual(tok.value, ':')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '1')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COMMA', tok.type)
        self.assertEqual(tok.value, ',')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'b')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COLON', tok.type)
        self.assertEqual(tok.value, ':')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '2')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COMMA', tok.type)
        self.assertEqual(tok.value, ',')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'c')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COLON', tok.type)
        self.assertEqual(tok.value, ':')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '3')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'RBRACE', tok.type)
        self.assertEqual(tok.value, '}')



    def test_parens(self):
        """Test parens

        (1 + 2)
        (a / (b / (c / d)))
        """
        lines = self.get_lines(self.test_parens)

        # (1 + 2)
        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'LPAREN', tok.type)
        self.assertEqual(tok.value, '(')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '1')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'PLUS', tok.type)
        self.assertEqual(tok.value, '+')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '2')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'RPAREN', tok.type)
        self.assertEqual(tok.value, ')')

        # (a / (b / (c / d)))
        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'LPAREN', tok.type)
        self.assertEqual(tok.value, '(')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'a')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'DIV', tok.type)
        self.assertEqual(tok.value, '/')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'LPAREN', tok.type)
        self.assertEqual(tok.value, '(')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'b')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'DIV', tok.type)
        self.assertEqual(tok.value, '/')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'LPAREN', tok.type)
        self.assertEqual(tok.value, '(')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'c')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'DIV', tok.type)
        self.assertEqual(tok.value, '/')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'd')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'RPAREN', tok.type)
        self.assertEqual(tok.value, ')')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'RPAREN', tok.type)
        self.assertEqual(tok.value, ')')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'RPAREN', tok.type)
        self.assertEqual(tok.value, ')')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')

        assert self.lexer.token().type == 'ENDMARKER'
        assert self.lexer.token() is None


    def test_booleans(self):
        u"""Test operators

        foo e bar
        b ou c
        nao var_true
        """
        lines = self.get_lines(self.test_booleans)

        # a and b
        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'foo')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'BAND', tok.type)
        self.assertEqual(tok.value, 'e')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'bar')

        # b or c
        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'b')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'BOR', tok.type)
        self.assertEqual(tok.value, 'ou')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'c')

        # not var_true
        self.lexer.input(lines.next())
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'BNOT', tok.type)
        self.assertEqual(tok.value, 'nao')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'var_true')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')

        assert self.lexer.token().type == 'ENDMARKER'
        assert self.lexer.token() is None

    def test_membership_and_identity(self):
        """Test if membership and identity testing works

        a in b
        a not in b
        a is b
        a is not b
        """
        string = self.get_string(self.test_membership_and_identity)
        self.lexer.input(string)

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'a')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'IN', tok.type)
        self.assertEqual(tok.value, 'in')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'b')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'a')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'BNOT', tok.type)
        self.assertEqual(tok.value, 'not')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'IN', tok.type)
        self.assertEqual(tok.value, 'in')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'b')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'a')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'IS', tok.type)
        self.assertEqual(tok.value, 'is')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'b')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'a')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'IS', tok.type)
        self.assertEqual(tok.value, 'is')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'BNOT', tok.type)
        self.assertEqual(tok.value, 'not')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'b')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n\n')

    def test_if_indent_dedent(self):
        """Test if statement and indent, dedent tokens

        se a < b:
            c = b
        entao:
            c = d
        x = c
        """
        string = self.get_string(self.test_if_indent_dedent)

        self.lexer.input(string)

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'IF', tok.type)
        self.assertEqual(tok.value, 'se')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'a')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'LT', tok.type)
        self.assertEqual(tok.value, '<')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'b')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COLON', tok.type)
        self.assertEqual(tok.value, ':')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'INDENT', tok.type)
        self.assertEqual(tok.value, None)
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'c')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ASSIGN', tok.type)
        self.assertEqual(tok.value, '=')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'b')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'DEDENT', tok.type)
        self.assertEqual(tok.value, None)

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ELSE', tok.type)
        self.assertEqual(tok.value, 'entao')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COLON', tok.type)
        self.assertEqual(tok.value, ':')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'INDENT', tok.type)
        self.assertEqual(tok.value, None)
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'c')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ASSIGN', tok.type)
        self.assertEqual(tok.value, '=')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'd')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'DEDENT', tok.type)
        self.assertEqual(tok.value, None)

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'x')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ASSIGN', tok.type)
        self.assertEqual(tok.value, '=')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'c')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')

        assert self.lexer.token().type == 'ENDMARKER'
        assert self.lexer.token() is None


    def test_no_indent_in_parens(self):
        """Test it doesn't generate newlines and indents inside parens

        a = (1 + 2,
             3 + 4
             )
        """
        string = self.get_string(self.test_no_indent_in_parens)

        self.lexer.input(string)

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'a')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ASSIGN', tok.type)
        self.assertEqual(tok.value, '=')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'LPAREN', tok.type)
        self.assertEqual(tok.value, '(')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '1')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'PLUS', tok.type)
        self.assertEqual(tok.value, '+')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '2')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COMMA', tok.type)
        self.assertEqual(tok.value, ',')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '3')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'PLUS', tok.type)
        self.assertEqual(tok.value, '+')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ICONST', tok.type)
        self.assertEqual(tok.value, '4')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'RPAREN', tok.type)
        self.assertEqual(tok.value, ')')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n\n')

        assert self.lexer.token().type == 'ENDMARKER'
        assert self.lexer.token() is None


    def test_indent_error(self):
        """Test indent fails in a must indent code

        if a:
        a = 0
        """
        string = self.get_string(self.test_indent_error)

        self.lexer.input(string)

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'IF', tok.type)
        self.assertEqual(tok.value, 'if')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'a')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COLON', tok.type)
        self.assertEqual(tok.value, ':')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')
        self.assertRaises(IndentationError, self.lexer.token)

    def test_for_indent_dedent(self):
        """Test 'for', 'in' and indent, dedent tokens

        para a em b:
            x = a
        """
        string = self.get_string(self.test_for_indent_dedent)

        self.lexer.input(string)
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'FOR', tok.type)
        self.assertEqual(tok.value, 'para')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'a')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'IN', tok.type)
        self.assertEqual(tok.value, 'em')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'b')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'COLON', tok.type)
        self.assertEqual(tok.value, ':')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n')

        tok = self.lexer.token()
        self.assertEqual(tok.type, 'INDENT', tok.type)
        self.assertEqual(tok.value, None)
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'x')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'ASSIGN', tok.type)
        self.assertEqual(tok.value, '=')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NAME', tok.type)
        self.assertEqual(tok.value, 'a')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'NEWLINE', tok.type)
        self.assertEqual(tok.value, '\n\n')
        tok = self.lexer.token()
        self.assertEqual(tok.type, 'DEDENT', tok.type)
        self.assertEqual(tok.value, None)

        assert self.lexer.token().type == 'ENDMARKER'
        assert self.lexer.token() is None



if __name__ == '__main__':
    unittest.main()


