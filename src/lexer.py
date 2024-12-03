import ply.lex as ply_lex
import re

def get_all_tokens(lexer, program):
    """Obtiene todos los tokens del programa dado."""
    lexer.input(program)
    return [(token.type, token.value) for token in iter(lambda: lexer.token(), None)]
   
class Lexer:
    """Clase que define el analizador léxico para el lenguaje."""
    tokens = [
        'LOWERID', 'UPPERID', 'NUMBER', 'CHAR', 'STRING',
        'DEFEQ', 'SEMICOLON', 'LPAREN', 'RPAREN', 'LAMBDA', 'PIPE', 'ARROW',
        'AND', 'OR', 'NOT', 'EQ', 'NE', 'GE', 'LE', 'GT', 'LT',
        'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD'] + [
        'DEF', 'IF', 'THEN', 'ELIF', 'ELSE', 'CASE', 'LET', 'IN'
    ]
    keywords = {
            'def': 'DEF',
            'if': 'IF',
            'then': 'THEN',
            'elif': 'ELIF',
            'else': 'ELSE',
            'case': 'CASE',
            'let': 'LET',
            'in': 'IN',
        }
    t_ignore = ' \t'
    t_SEMICOLON, t_LPAREN, t_RPAREN = r';', r'\(', r'\)'
    t_ARROW, t_LAMBDA, t_AND = r'->', r'\\', r'&&'
    t_OR, t_NOT, t_EQ = r'\|\|', r'!', r'=='
    t_NE, t_GE, t_LE = r'!=', r'>=', r'<='
    t_GT, t_LT, t_PLUS = r'>', r'<', r'\+'
    t_MINUS, t_TIMES, t_DIV = r'-', r'\*', r'/'
    t_MOD, t_PIPE, t_DEFEQ = r'%', r'\|', r'='

    esc_chars = {"\\n": '\n', "\\r": '\r', "\\t": '\t', "\\\\": '\\', '\\"': '"', "\\'": "'"}

    def t_CHAR(self, t):
        r"""\'(?P<value>(\\[ntr\\\'\"])|[^\\\'])\'"""
        t.value = self.esc_chars.get(t.lexer.lexmatch.group('value'), t.lexer.lexmatch.group('value'))
        return t

    def t_STRING(self, t):
        r"""\"(?P<value>((\\[ntr\\\'\"])|[^\\\"])*)\""""
        t.value = re.sub(r'\\[ntr\\\'\"]', lambda x: self.esc_chars[x.group(0)], t.lexer.lexmatch.group('value'))
        return t

    def t_LOWERID(self, t):
        r"""[a-z][_a-zA-Z0-9]*"""
        t.type = 'LOWERID' if t.value not in self.keywords else self.keywords[t.value]
        return t

    def t_UPPERID(self, t):
        r"""[A-Z][_a-zA-Z0-9]*"""
        t.type = 'UPPERID' if t.value not in self.keywords else self.keywords[t.value]
        return t

    def t_NUMBER(self, t):
        r"""\d+"""
        t.value = int(t.value)
        return t

    def t_comment(self, t):
        r"""\--.*\n?"""
        t.lexer.lineno += 1

    def t_ignore_newline(self, t):
        r"""\n+"""
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print(f'Error: carácter ilegal {t.value[0]!r}')
        t.lexer.skip(1)

    def build(self):
        return ply_lex.lex(module=self)