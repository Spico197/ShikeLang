import shikelang.ply.lex as lex

# LEX for parsing Python

# Tokens
tokens = (
    # values
    "VARIABLE",
    "NUMBER",
    "BOOL",
    "STRING",
    # math
    "GDIV",
    # controls
    "IF",
    "ELIF",
    "ELSE",
    "WHILE",
    "FOR",
    "INC",
    "BREAK",
    "DO",
    "UNTIL",
    # func
    "LEN",
    "DEATH",
    "BIRTH",
    # args
    "VOID",
    # print
    "SHIT",
    # brackets
    "LCLOSE",
    "RCLOSE",
    # comparison
    "LET",
    "GET",
    "EQ",
    # types
    "TYPE",
)

literals = ["=", "+", "-", "*", "(", ")", "{", "}", "<", ">", ";", "!", ",", "[", "]"]

# Define of tokens
def t_BIRTH(t):
    r"birth"
    return t


def t_DEATH(t):
    r"death"
    return t


def t_VOID(t):
    r"void"
    return t


def t_LCLOSE(t):
    r"[\{\[\(<]"
    return t


def t_RCLOSE(t):
    r"[\)\]\}]"
    return t


def t_BOOL(t):
    r"(true|false)"
    return t


def t_STRING(t):
    r"[\"'].*?[\"']"
    return t


def t_TYPE(t):
    r"(bool|int)"
    return t


def t_NUMBER(t):
    r"[0-9]+"
    return t


def t_DO(t):
    r"do"
    return t


def t_UNTIL(t):
    r"until"
    return t


def t_SHIT(t):
    r"shit"
    return t


def t_IF(t):
    r"if"
    return t


def t_WHILE(t):
    r"while"
    return t


def t_FOR(t):
    r"for"
    return t


def t_LEN(t):
    r"len"
    return t


def t_INC(t):
    "\+\+"
    return t


def t_GDIV(t):
    r"//"
    return t


def t_BREAK(t):
    r"break"
    return t


def t_LET(t):
    r"<="
    return t


def t_GET(t):
    r">="
    return t


def t_EQ(t):
    r"=="
    return t


def t_ELIF(t):
    r"elif"
    return t


def t_ELSE(t):
    r"else"
    return t


def t_VARIABLE(t):
    r"[a-zA-Z_]+"
    return t


# Ignored
t_ignore = " \t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lex_obj = lex.lex()
