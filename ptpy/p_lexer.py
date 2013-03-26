# -*- coding: utf-8 -*-
#
# contributor : Pedro Werneck
# name : Python file template .... :

__author__ = "Pedro Werneck (pjwerneck@gmail.com)"
__date__ = "Sat Sep 29 00:21:50 2012"


import re

import ply.lex as lex



# Reserved words
RESERVED = {
    'e': 'BAND',  # and
    'garantir': 'ASSERT',  # assert
    'interromper': 'BREAK',  # break
    'classe': 'CLASS',  # class
    'continuar': 'CONTINUE',  # continue
    'define': 'DEF',  # def
    'apagar': 'DEL',  # del
    'senao': 'ELIF',  # elif
    'else': 'ELSE',  # else
    'exceto': 'EXCEPT',  # except
    'executar': 'EXEC',  # exec
    'finalmente': 'FINALLY',  # finally
    'para': 'FOR',  # for
    'de': 'FROM',  # from
    'global': 'GLOBAL',  # global
    'se': 'IF',  # if
    'importar': 'IMPORT',  # import
    'em': 'IN',  # in
    'is': 'IS',  # is
    'lambda': 'LAMBDA',  # lambda
    'nao': 'BNOT',  # not
    'ou': 'BOR',  # or
    'passar': 'PASS',  # pass
    'exibir': 'PRINT',  # print
    'raise': 'RAISE',  # raise
    'retornar': 'RETURN',  # return
    'tentar': 'TRY',  # try
    'enquanto': 'WHILE',  # while
}



# List of token names.   This is always required
tokens = RESERVED.values() + [
    # literals, identifies, constants
    'NAME',
    'ICONST',
    'FCONST',
    'SCONST',

    # delimiters
    'COLON',
    'COMMA',
    'SEMICOLON',
    'DOT',

    # brackets
    'LPAREN',   # (
    'RPAREN',   # )
    'LBRACKET', # [
    'RBRACKET', # ]
    'LBRACE',   # {
    'RBRACE',   # }

    # operators
    'PLUS',  # +
    'MINUS', # -
    'MULT',  # *
    'DIV',   # /
    'MOD',   # %
    'POW',   # **
    'OR',    # |
    'AND',   # &
    'NOT',   # ~
    'XOR',   # ^
    'LSHIFT',# <<
    'RSHIFT',# >>
    'LT',    # <
    'LE',    # <=
    'GT',    # >
    'GE',    # >=
    'EQ',    # ==
    'NE',    # !=

    # assignment
    'ASSIGN',  # =
    'IPLUS',   # +=
    'IMINUS',  # -=
    'IDIV',    # /=
    'IMUL',    # *=
    'IMOD',    # %=
    'IPOW',    # **=
    'ILSHIFT', # <<=
    'IRSHIFT', # >>=
    'IAND',    # &=
    'IOR',     # |=
    'INOT',    # ~=
    'IXOR',    # ^=

    # whitespace
    'WS',
    'NEWLINE',

    # indenting
    'INDENT',
    'DEDENT',
    'ENDMARKER',
]


# integer literal
t_ICONST = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# floating literal
t_FCONST = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# string literal
#t_SCONST = r'\"([^\\\n]|(\\.))*?\"'

# delimiters
t_COLON = r':'
t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'

# operators
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_MULT   = r'\*'
t_DIV    = r'/'
t_MOD    = r'%'
t_POW    = r'\*\*'
t_OR     = r'\|'
t_AND    = r'&'
t_NOT    = r'~'
t_XOR    = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_LT     = r'<'
t_LE     = r'<='
t_GT     = r'>'
t_GE     = r'>='
t_EQ     = r'=='
t_NE     = r'!='

# assignment
t_ASSIGN  = r'='
t_IPLUS   = r'\+='
t_IMINUS  = r'-='
t_IDIV    = r'/='
t_IMUL    = r'\*='
t_IMOD    = r'%='
t_IPOW    = r'\*\*='
t_ILSHIFT = r'<<='
t_IRSHIFT = r'>>='
t_IAND    = r'&='
t_IOR     = r'\|='
t_IXOR    = r'\^='
t_INOT    = r'~='

t_IS = r'is'
t_IN = r'in'



# Error handling rule
def t_error(t):
    raise SyntaxError("Illegal character %r, (%i, %i)" % (t.value[0], t.lineno, t.lexpos))

    t.lexer.skip(1)


## Putting this before t_WS let it consume lines with only comments in
# them so the latter code never sees the WS part.  Not consuming the
# newline.  Needed for "if 1: #comment"
def t_COMMENT(t):
    r"[ ]*\043[^\n]*"  # \043 is '#'


def t_SCONST(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1].decode("string-escape")
    return t

# whitespace
def t_WS(t):
    r' [ ]+ '
    if t.lexer.at_line_start and t.lexer.paren_count == 0:
        return t


# Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    try:
        if t.lexer.paren_count == 0:
            return t
    except AttributeError:
        return t


# identifiers
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = RESERVED.get(t.value, "NAME")
    return t


# parenthesis
def t_LPAREN(t):
    r'\('
    try:
        t.lexer.paren_count += 1
    except AttributeError:
        t.lexer.paren_count = 1
    return t


def t_RPAREN(t):
    r'\)'
    # check for underflow?  should be the job of the parser
    t.lexer.paren_count -= 1
    return t

# brackets
def t_LBRACKET(t):
    r'\['
    try:
        t.lexer.bracket_count += 1
    except AttributeError:
        t.lexer.bracket_count = 1
    return t

def t_RBRACKET(t):
    r'\]'
    t.lexer.bracket_count -= 1
    return t

# braces
def t_LBRACE(t):
    r'\{'
    try:
        t.lexer.brace_count += 1
    except AttributeError:
        t.lexer.brace_count = 1
    return t

def t_RBRACE(t):
    r'\}'
    t.lexer.brace_count -= 1
    return t


## I implemented INDENT / DEDENT generation as a post-processing filter

# The original lex token stream contains WS and NEWLINE characters.
# WS will only occur before any other tokens on a line.

# I have three filters.  One tags tokens by adding two attributes.
# "must_indent" is True if the token must be indented from the
# previous code.  The other is "at_line_start" which is True for WS
# and the first non-WS/non-NEWLINE on a line.  It flags the check so
# see if the new line has changed indication level.

# Python's syntax has three INDENT states
#  0) no colon hence no need to indent
#  1) "if 1: go()" - simple statements have a COLON but no need for an indent
#  2) "if 1:\n  go()" - complex statements have a COLON NEWLINE and must indent
NO_INDENT = 0
MAY_INDENT = 1
MUST_INDENT = 2

def track_tokens_filter(lexer, tokens):
    lexer.at_line_start = at_line_start = True
    indent = NO_INDENT
    saw_colon = False
    for token in tokens:
        token.at_line_start = at_line_start

        if token.type == "COLON":
            at_line_start = False
            indent = MAY_INDENT
            token.must_indent = False

        elif token.type == "NEWLINE":
            at_line_start = True
            if indent == MAY_INDENT:
                indent = MUST_INDENT
            token.must_indent = False

        elif token.type == "WS":
            assert token.at_line_start == True
            at_line_start = True
            token.must_indent = False

        else:
            # A real token; only indent after COLON NEWLINE
            if indent == MUST_INDENT:
                token.must_indent = True
            else:
                token.must_indent = False
            at_line_start = False
            indent = NO_INDENT

        yield token
        lexer.at_line_start = at_line_start


def _new_token(type, lineno, lexpos=-1):
    tok = lex.LexToken()
    tok.type = type
    tok.value = None
    tok.lineno = lineno
    tok.lexpos = lexpos
    return tok


def _add_endmarker(token_stream):
    "Put a sentinel marker at the end of the token_stream"
    tok = None
    for tok in token_stream:
        yield tok
    if tok is not None:
        lineno = tok.lineno
    else:
        lineno = 1
    yield _new_token("ENDMARKER", lineno, tok.lexpos+1)


# Synthesize a DEDENT tag
def DEDENT(lineno):
    return _new_token("DEDENT", lineno)


# Synthesize an INDENT tag
def INDENT(lineno):
    return _new_token("INDENT", lineno)


# Track the indentation level and emit the right INDENT / DEDENT events.
def indentation_filter(tokens):
    # A stack of indentation levels; will never pop item 0
    levels = [0]
    token = None
    depth = 0
    prev_was_ws = False
    for token in tokens:
        # WS only occurs at the start of the line
        # There may be WS followed by NEWLINE so
        # only track the depth here.  Don't indent/dedent
        # until there's something real.
        if token.type == "WS":
            assert depth == 0
            depth = len(token.value)
            prev_was_ws = True
            # WS tokens are never passed to the parser
            continue

        if token.type == "NEWLINE":
            depth = 0
            if prev_was_ws or token.at_line_start:
                # ignore blank lines
                continue
            # pass the other cases on through
            yield token
            continue

        # then it must be a real token (not WS, not NEWLINE)
        # which can affect the indentation level

        prev_was_ws = False
        if token.must_indent:
            # The current depth must be larger than the previous level
            if not (depth > levels[-1]):
                raise IndentationError("expected an indented block")

            levels.append(depth)
            yield INDENT(token.lineno)

        elif token.at_line_start:
            # Must be on the same level or one of the previous levels
            if depth == levels[-1]:
                # At the same level
                pass
            elif depth > levels[-1]:
                raise IndentationError("indentation increase but not in new block")
            else:
                # Back up; but only if it matches a previous level
                try:
                    i = levels.index(depth)
                except ValueError:
                    raise IndentationError("inconsistent indentation")
                for _ in range(i+1, len(levels)):
                    yield DEDENT(token.lineno)
                    levels.pop()

        yield token

    # Must dedent any remaining levels
    if len(levels) > 1:
        assert token is not None
        for _ in range(1, len(levels)):
            yield DEDENT(token.lineno)



# Wrap everything into a new lexer
class PtpyLexer(object):
    def __init__(self, debug=0, optimize=0, lextab='lextab', reflags=0):
        self.lexer = lex.lex(debug=debug,
                             optimize=optimize,
                             lextab=lextab,
                             reflags=reflags)

        self.token_stream = None

    def input(self, data, add_endmarker=True):
        data = data + '\n#' # FIXME!!!! PLEASE!!!
        # for some reason, parser don't get endmarker if there's not a
        # comment at the end of the stream
        self.lexer.paren_count = 0
        self.lexer.bracket_count = 0
        self.lexer.brace_count = 0

        self.lexer.input(data)

        tokens = iter(self.lexer.token, None)
        tokens = track_tokens_filter(self.lexer, tokens)
        tokens = indentation_filter(tokens)

        if add_endmarker:
            tokens = _add_endmarker(tokens)

        self.token_stream = tokens

    def token(self):
        try:
            return self.token_stream.next()
        except StopIteration:
            return None

    def __iter__(self):
        return self.token_stream



if __name__ == '__main__':
    lexer = PtpyLexer(reflags=re.UNICODE)

    data = raw_input()


    print repr(data)

    lexer.input(data)

    while 1:
        tok = lexer.token()
        if not tok:
            break
        print tok.type, repr(tok.value)
