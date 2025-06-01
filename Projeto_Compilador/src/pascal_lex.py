import ply.lex as lex

# Coments { this is a comment}
def t_COMMENT_BRACKETS(t):
    r'\{(.|\n)*?\}'
    t.lexer.lineno += t.value.count('\n')

# Comments (* This is also a comment*)
def t_COMMENT_PARENTESIS(t):
    r'\(\*(.|\n)*?\*\)'
    t.lexer.lineno += t.value.count('\n')


reserved = {
    'and': 'AND',
    'begin': 'BEGIN',
    #    'case': 'CASE',
    #    'const': 'CONST',
    'do': 'DO',
    #    'downto': 'DOWNTO',
    'else': 'ELSE',
    'end': 'END',
    #    'file': 'FILE',
    'false': 'FALSE',
    'for': 'FOR',
    #    'function': 'FUNCTION',
    #    'goto': 'GOTO',
    'if': 'IF',
    #    'in': 'IN',
    'real': 'REAL',
    'integer': 'INTEGER',
    'string': 'STRING',
    'boolean': 'BOOLEAN',
    #    'label': 'LABEL',
    #    'nil': 'NIL',
    'not': 'NOT',
    'of': 'OF',
    'or': 'OR',
    #    'packed': 'PACKED',
    #    'procedure': 'PROCEDURE',
    'program': 'PROGRAM',
    #    'record': 'RECORD',
    #    'repeat': 'REPEAT',
    #    'set': 'SET',
    'then': 'THEN',
    'to': 'TO',
    'true':  'TRUE',
    #    'type': 'TYPE',
    #    'until': 'UNTIL',
    #    'uses': 'USES',
    'var': 'VAR',
    'while': 'WHILE',
    #    'with': 'WITH',
    'array': 'ARRAY',  # Array keyword
    'write': 'WRITE',  # Write keyword
    'writeln': 'WRITELN',
    'readln': 'READLN'
}


tokens = [
             'NUM_REAL',
             'NUM',
             'STR',
             'ATRIB',
             'VARNAME',
             # Relational operators:
             'EQUALS', 'NE', 'LT', 'LE', 'GT', 'GE'
         ] + list(reserved.values())

literals = ['+', '-', '*', '%', '/', ';', '(', ')', '[', ']', '.', ',', ':']

# Precedence declarations
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQUALS', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('right', 'UMINUS', 'NOT'),
)


# Token for assignment operator ":="
def t_ATRIB(t):
    r':='
    return t


# Tokens for relational operators.
def t_NE(t):
    r'<>'
    t.type = 'NE'
    return t


def t_LE(t):
    r'<='
    t.type = 'LE'
    return t


def t_GE(t):
    r'>='
    t.type = 'GE'
    return t


def t_LT(t):
    r'<'
    t.type = 'LT'
    return t


def t_GT(t):
    r'>'
    t.type = 'GT'
    return t


def t_EQUALS(t):
    r'='
    t.type = 'EQUALS'
    return t


def t_NUM_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


# Token for numbers.
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Token for strings.
def t_STRING(t):
    r'\'[^\']*?\''
    t.value = t.value[1:-1]
    return t


# Token for identifiers (or reserved words).
def t_VARNAME(t):
    r"[A-Za-z][A-Za-z0-9]*"
    t.type = reserved.get(t.value.lower(), 'VARNAME')
    return t


# Newline rule.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Ignore spaces and tabs.
t_ignore = " \t"


# Error handling.
def t_error(t):
    print("Caráter inválido, \"", t.value[0] + "\" na linha: ", t.lineno)
    t.lexer.skip(1)


lexer = lex.lex()
lexer.lineno = 1
