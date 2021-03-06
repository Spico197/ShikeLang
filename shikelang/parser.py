import shikelang.ply.yacc as yacc
from shikelang.tokenizer import *
from shikelang.node import Node, bool_node, num_node, string_node


def simple_node(t, name):
    t[0] = Node(name)
    for i in range(1, len(t)):
        if t.slice[i].type == "slice":
            t[0].add(t[i])
        elif t.slice[i].type == "NUMBER":
            t[0].add(num_node(t[i]))
        elif t.slice[i].type == "STRING":
            t[0].add(string_node(t[i]))
        else:
            t[0].add(Node(t[i]))
    return t[0]


def p_program(t):
    """program : VOID BIRTH LCLOSE VOID RCLOSE LCLOSE statements DEATH LCLOSE RCLOSE '!' RCLOSE"""
    t[0] = Node("[PROGRAM]")
    t[0].add(t[7])


def p_statements(t):
    """statements : statements statement
    | statement"""
    if len(t) == 3:
        t[0] = Node("[STATEMENTS]")
        t[0].add(t[1])
        t[0].add(t[2])
    elif len(t) == 2:
        t[0] = Node("[STATEMENTS]")
        t[0].add(t[1])


def p_statement(t):
    """statement : declaration '!'
    | assignment '!'
    | operation
    | shit  '!'
    | if
    | while
    | dountil
    | for
    | BREAK '!'"""
    t[0] = Node(["STATEMENT"])
    if t.slice[1].type == "BREAK":
        t[0].add(Node("[BREAK]"))
    else:
        t[0].add(t[1])


def p_declaration(t):
    """declaration : TYPE assignment"""
    t[0] = Node("[DECLARATION]")
    t[0].add(Node(t[1]))
    t[0].add(t[2])


def p_assignment(t):
    """assignment : VARIABLE '=' NUMBER
    | VARIABLE '=' VARIABLE
    | VARIABLE '=' operation
    | slice '=' slice
    | slice '=' VARIABLE
    | VARIABLE '=' slice
    | VARIABLE '=' BOOL
    | slice '=' BOOL
    | VARIABLE '=' STRING
    | slice '=' STRING"""
    if t.slice[1].type == "slice" or t.slice[3].type == "slice":
        t[0] = Node("[ASSIGNMENT]")
        if t.slice[1].type == "slice":
            if t.slice[3].type == "slice":
                t[0].add(t[1])
                t[0].add(Node(t[2]))
                t[0].add(t[3])
            else:
                t[0].add(t[1])
                t[0].add(Node(t[2]))
                t[0].add(Node(t[3]))
        else:
            t[0].add(Node(t[1]))
            t[0].add(Node(t[2]))
            t[0].add(t[3])
    elif t.slice[3].type == "operation":
        t[0] = Node("[ASSIGNMENT]")
        t[0].add(Node(t[1]))
        t[0].add(Node(t[2]))
        t[0].add(t[3])
    elif t.slice[3].type == "NUMBER":
        t[0] = Node("[ASSIGNMENT]")
        t[0].add(Node(t[1]))
        t[0].add(Node(t[2]))
        t[0].add(num_node(t[3]))
        # breakpoint()
    elif t.slice[3].type == "VARIABLE":
        t[0] = Node("[ASSIGNMENT]")
        t[0].add(Node(t[1]))
        t[0].add(Node(t[2]))
        t[0].add(Node(t[3]))
    elif t.slice[3].type == "BOOL":
        t[0] = Node("[ASSIGNMENT]")
        if t.slice[1].type == 'slice':
            t[0].add(t[1])
        else:
            t[0].add(Node(t[1]))
        t[0].add(Node(t[2]))
        t[0].add(bool_node(t[3]))
    elif t.slice[3].type == "STRING":
        t[0] = Node("[ASSIGNMENT]")
        if t.slice[1].type == 'slice':
            t[0].add(t[1])
        else:
            t[0].add(Node(t[1]))
        t[0].add(Node(t[2]))
        t[0].add(string_node(t[3]))


def p_slice(t):
    """slice : VARIABLE '[' VARIABLE ']' """
    t[0] = simple_node(t, "[SLICE]")


def p_commaexpression(t):
    """commaexpression : commaexpression ',' NUMBER
    | NUMBER ',' NUMBER
    | NUMBER"""
    if len(t) == 2:
        t[0] = Node("[COMMAEXPRESSION]")
        t[0].add(num_node(t[1]))
    elif len(t) == 4:
        t[0] = Node("[COMMAEXPRESSION]")
        if t.slice[1].type == "NUMBER":
            t[0].add(num_node(t[1]))
            t[0].add(num_node(t[3]))
        else:
            t[0].add(t[1])
            t[0].add(num_node(t[3]))


def p_operation(t):
    """operation : VARIABLE '+' VARIABLE
    | VARIABLE '-' VARIABLE
    | VARIABLE '-' NUMBER
    | VARIABLE '+' NUMBER
    | '[' commaexpression ']'
    | LEN '(' VARIABLE ')'
    | '(' VARIABLE '+' VARIABLE ')' GDIV NUMBER"""
    if len(t) == 4 and t.slice[2].type != "commaexpression":
        t[0] = simple_node(t, "[OPERATION]")
    elif len(t) == 4 and t.slice[2].type == "commaexpression":
        t[0] = Node("[OPERATION]")
        t[0].add(Node(t[1]))
        t[0].add(t[2])
        t[0].add(Node(t[3]))
    elif len(t) == 5:
        t[0] = simple_node(t, "[OPERATION]")
    elif len(t) == 8:
        t[0] = simple_node(t, "[OPERATION]")


def p_shit(t):
    """shit : SHIT LCLOSE VARIABLE RCLOSE
            | SHIT LCLOSE STRING RCLOSE """
    t[0] = simple_node(t, "[SHIT]")


def p_if(t):
    r"""if : IF LCLOSE condition RCLOSE LCLOSE statements RCLOSE
    | IF LCLOSE condition RCLOSE LCLOSE statements RCLOSE ELIF LCLOSE condition RCLOSE LCLOSE statements RCLOSE ELSE LCLOSE statements RCLOSE"""
    if len(t) == 8:
        t[0] = Node("[IF]")
        t[0].add(t[3])
        t[0].add(t[6])
    else:
        t[0] = Node("[IF]")
        t[0].add(t[3])  # condition
        t[0].add(t[6])  # statements
        t[0].add(t[10])  # condition
        t[0].add(t[13])  # statements
        t[0].add(t[17])  # break


def p_condition(t):
    """condition : VARIABLE EQ VARIABLE
                | VARIABLE EQ BOOL
                | VARIABLE '>' VARIABLE
                | VARIABLE '<' VARIABLE
                | VARIABLE LET VARIABLE
                | VARIABLE GET VARIABLE
                | slice EQ VARIABLE
                | slice EQ BOOL
                | slice '>' VARIABLE
                | slice '<' VARIABLE
                | slice LET VARIABLE
                | slice GET VARIABLE
                | VARIABLE EQ NUMBER
                | VARIABLE '>' NUMBER
                | VARIABLE '<' NUMBER
                | VARIABLE LET NUMBER
                | VARIABLE GET NUMBER
                | slice EQ NUMBER
                | slice '>' NUMBER
                | slice '<' NUMBER
                | slice LET NUMBER
                | slice GET NUMBER"""
    t[0] = simple_node(t, "[CONDITION]")


def p_while(t):
    r"""while : WHILE LCLOSE condition RCLOSE LCLOSE statements RCLOSE"""
    if len(t) == 8:
        t[0] = Node("[WHILE]")
        t[0].add(t[3])
        t[0].add(t[6])


def p_dountil(t):
    r"""dountil : DO LCLOSE statements RCLOSE UNTIL LCLOSE condition RCLOSE"""
    t[0] = Node("[DO_UNTIL]")
    t[0].add(t[3])
    t[0].add(t[7])


def p_for(t):
    r"""for : FOR LCLOSE assignment ';' condition ';' VARIABLE INC RCLOSE LCLOSE statements RCLOSE"""
    t[0] = Node("[FOR]")
    t[0].add(t[3])
    t[0].add(t[5])
    t[0].add(Node(t[7]))
    t[0].add(t[11])


def p_error(t):
    print(
        f"Syntax error at lineno: {t.lineno}, lexpos: {t.lexpos}, type:  {t.type}, value: {t.value}"
    )


parser = yacc.yacc()
