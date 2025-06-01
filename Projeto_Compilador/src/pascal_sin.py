import sys
import ply.yacc as yacc
from pascal_lex import tokens, literals, lexer, precedence

dic = {}
syntax_errors = []


#######################
#  Pascal Program Rule
#######################
def p_Program(p):
    "Program : PROGRAM VARNAME ';' Code '.'"
    p[0] = ('program', p[2], p[4])


####################
# Code and Declarations
####################
def p_Code(p):
    "Code : Declarations CompoundStatement"
    p[0] = ('code', p[1], p[2])


# Allow empty declarations
def p_Declarations_empty(p):
    "Declarations :"
    p[0] = None


# Variable declarations: e.g., VAR a, b : INTEGER;
def p_Declarations_var(p):
    "Declarations : VAR VariableList"
    p[0] = ('var_decls', p[2])


def p_VariableList_single(p):
    "VariableList : VariableDeclaration"
    p[0] = [p[1]]


def p_VariableList_multiple(p):
    "VariableList : VariableList VariableDeclaration"
    p[0] = p[1] + [p[2]]


def p_VariableDeclaration(p):
    "VariableDeclaration : IdentifierList ':' DataType ';'"
    for var in p[1]:
        if p[3] == "integer":
            dic[var] = (0, "integer")
        if p[3] == "boolean":
            dic[var] = ('true', "boolean")
        if p[3] == "string":
            dic[var] = ('', "string")
        if p[3] == "real":
            dic[var] = (0.0, "real")
        elif isinstance(p[3], tuple) and p[3][0] == 'array':
            low, high = p[3][1]
            size = high - low + 1
            # print(var)
            dic[var] = ([0] * size, p[3])
        else:
            dic[var] = (None, p[3])
    p[0] = ('decl', p[1], p[3])


def p_IdentifierList_single(p):
    "IdentifierList : VARNAME"
    p[0] = [p[1]]


def p_IdentifierList_multiple(p):
    "IdentifierList : IdentifierList ',' VARNAME"
    p[0] = p[1] + [p[3]]


def p_DataType_integer(p):
    "DataType : INTEGER"
    p[0] = "integer"


def p_DataType_real(p):
    "DataType : REAL"
    p[0] = "real"


def p_DataType_boolean(p):
    "DataType : BOOLEAN"
    p[0] = "boolean"


def p_DataType_string(p):
    "DataType : STRING"
    p[0] = "string"


def p_DataType_array(p):
    "DataType : ARRAY '[' NUM '.' '.' NUM ']' OF DataType"
    p[0] = ('array', (p[3], p[6]), p[9])


#########################
# New Statement Grammar (handling dangling else)
#########################
# A statement is either a fully matched statement (if with else) or an unmatched if.
def p_Statement(p):
    """Statement : MatchedStatement
                 | UnmatchedStatement
    """
    p[0] = p[1]


# A matched statement is either a complete if-then-else or any non-if statement.
def p_MatchedStatement_if(p):
    "MatchedStatement : IF Exp THEN MatchedStatement ELSE MatchedStatement"
    p[0] = ('if', p[2], ('then', p[4]), ('else', p[6]))


def p_MatchedStatement_nonif(p):
    "MatchedStatement : NonIfStatement"
    p[0] = p[1]


# NonIfStatement covers all statements that are not if-statements.
def p_NonIfStatement(p):
    """NonIfStatement : CompoundStatement
                      | RepetitiveStatement
                      | SingleStatement
    """
    p[0] = p[1]


# ...or an if where the else-part leads to an unmatched statement.
def p_UnmatchedStatement_ifelse(p):
    "UnmatchedStatement : IF Exp THEN MatchedStatement ELSE UnmatchedStatement"
    p[0] = ('if', p[2], ('then', p[4]), ('else', p[6]))


# An unmatched statement is an if without an else...
def p_UnmatchedStatement_if(p):
    "UnmatchedStatement : IF Exp THEN Statement"
    p[0] = ('if', p[2], ('then', p[4]), None)


#########################
# Other Statement Rules
#########################
# Modified to allow an optional semicolon after END.
def p_CompoundStatement(p):
    "CompoundStatement : BEGIN StatementList END OptionalSemicolon"
    p[0] = ('compound', p[2])


def p_StatementList_single(p):
    "StatementList : Statement"
    p[0] = [p[1]]


def p_StatementList_multiple(p):
    "StatementList : StatementList Statement"
    p[0] = p[1] + [p[2]]


def p_RepetitiveStatement_for(p):
    "RepetitiveStatement : FOR VARNAME ATRIB Exp TO Exp DO Statement"
    p[0] = ('for', p[2], p[4], p[6], p[8])


def p_RepetitiveStatement_while(p):
    "RepetitiveStatement : WHILE Exp DO Statement"
    p[0] = ('while', p[2], p[4])


def p_SingleStatement_assign(p):
    "SingleStatement : VARNAME ATRIB Exp OptionalSemicolon"
    if p[1] in dic:
        var_type = dic[p[1]][1]
        dic[p[1]] = (p[3], var_type)
    else:
        print(f"Error: variable {p[1]} not declared")
        dic[p[1]] = (p[3], None)
    p[0] = ('assign', p[1], p[3])

# Modified production: use OptionalSemicolon instead of a fixed semicolon.
def p_SingleStatement_writeln(p):
    "SingleStatement : WRITELN '(' ArgumentList ')' OptionalSemicolon"
    p[0] = ('writeln', p[3])
    # print("Writeln:", p[3])


def p_SingleStatement_writeln2(p):
    "SingleStatement : WRITELN OptionalSemicolon"
    p[0] = 'writeln'
    # print("Writeln:", p[3])


def p_SingleStatement_write(p):
    "SingleStatement : WRITE '(' ArgumentList ')' OptionalSemicolon"
    p[0] = ('write', p[3])
    # print("Write:", p[3])


def p_SingleStatement_readln(p):
    "SingleStatement : READLN '(' VARNAME ')' ';'"
    if p[3] in dic:
        dic[p[3]] = (0, dic[p[3]][1])
    else:
        dic[p[3]] = (0, None)
    p[0] = ('readln', p[3])


def p_SingleStatement_readln_array(p):
    "SingleStatement : READLN '(' VARNAME '[' Exp ']' ')' ';'"

    limit = dic[p[3]][1][1]

    a = limit[0]
    b = limit[1]

    if (isinstance(p[5], int)):
        value = p[5]

    elif isinstance(p[5][1], int) or isinstance(p[5][1], float):
        value = - p[5][1]
    else:
        value = p[5]

    if isinstance(value, int) and not value in range(a, b + 1):
        print("Warning: range check error while evaluating constants (", value, "must be between", a, "and", b, ")")
        parser.success = False

    p[0] = ('readln_array', p[3], p[5])


#########################
# Argument List (for WRITELN and WRITE)
#########################
def p_ArgumentList_single(p):
    "ArgumentList : Argument"
    p[0] = [p[1]]


def p_ArgumentList_multiple(p):
    "ArgumentList : ArgumentList ',' Argument"
    p[0] = p[1] + [p[3]]


def p_Argument_string(p):
    "Argument : STR"
    p[0] = p[1]


def p_Argument_exp(p):
    "Argument : Exp"
    p[0] = p[1]


def p_Argument_formatted(p):
    "Argument : Exp ':' FORMAT"
    p[0] = ('formatted', p[1], p[3])


def p_Format(p):
    "FORMAT : NUM"
    print("Format:", p[1])
    p[0] = p[1]


def p_complete_Format(p):
    "FORMAT : NUM ':' NUM"
    p[0] = (p[1], p[3])


#########################
# Expression Productions
#########################
def p_Expression_relop(p):
    "Exp : SimpleExpression RelOp SimpleExpression"
    p[0] = ('rel', p[2], p[1], p[3])

def p_Expression_and(p):
    "Exp : Exp AND Exp"
    p[0] = ('and', p[1], p[3])

def p_Expression_or(p):
    "Exp : Exp OR Exp"
    p[0] = ('or', p[1], p[3])


def p_Expression_simple(p):
    "Exp : SimpleExpression"
    p[0] = p[1]


def p_RelOp(p):
    """RelOp : EQUALS
             | NE
             | LT
             | LE
             | GT
             | GE
    """
    p[0] = p[1]


def p_SimpleExpression_sign(p):
    "SimpleExpression : '+' AdditiveExpression"
    p[0] = p[2]


def p_SimpleExpression_sign_neg(p):
    "SimpleExpression : '-' AdditiveExpression %prec UMINUS"
    p[0] = ('uminus', p[2])


def p_SimpleExpression(p):
    "SimpleExpression : AdditiveExpression"
    p[0] = p[1]


def p_AdditiveExpression_plus(p):
    "AdditiveExpression : AdditiveExpression '+' Term"
    p[0] = ('+', p[1], p[3])


def p_AdditiveExpression_minus(p):
    "AdditiveExpression : AdditiveExpression '-' Term"
    p[0] = ('-', p[1], p[3])


def p_AdditiveExpression_term(p):
    "AdditiveExpression : Term"
    p[0] = p[1]


def p_Term_mul(p):
    "Term : Term '*' Factor"
    p[0] = ('*', p[1], p[3])


def p_Term_div(p):
    "Term : Term '/' Factor"
    p[0] = ('/', p[1], p[3])


def p_Term_mod(p):
    "Term : Term '%' Factor"
    p[0] = ('%', p[1], p[3])


def p_Term_factor(p):
    "Term : Factor"
    p[0] = p[1]


def p_Factor_num(p):
    "Factor : NUM"
    p[0] = p[1]


def p_Factor_real(p):
    "Factor : NUM_REAL"
    p[0] = p[1]


def p_Factor_string(p):
    "Factor : STRING"
    p[0] = p[1]


def p_Factor_true(p):
    "Factor : TRUE"
    p[0] = 1

def p_Factor_false(p):
    "Factor : FALSE"
    p[0] = 0


def p_Factor_var(p):
    "Factor : VARNAME"
    p[0] = ('var', p[1])


def p_Factor_paren(p):
    "Factor : '(' Exp ')'"
    p[0] = p[2]


# array_access access_array
def p_Factor_array(p):
    "Factor : VARNAME '[' Exp ']'"
    limit = dic[p[1]][1][1]

    a = limit[0]
    b = limit[1]

    if isinstance(p[3], int):
        value = p[3]

    elif isinstance(p[3][1], int) or isinstance(p[3][1], float):
        value = - p[3][1]
    else:
        value = p[3]

    if isinstance(value, int) and not value in range(a, b + 1):
        print("Warning: range check error while evaluating constants (", value, "must be between", a, "and", b, ")")
        parser.success = False

    p[0] = ('array_access', p[1], p[3])


def p_Factor_not(p):
    "Factor : NOT Factor %prec NOT"
    p[0] = ('not', p[2])


#########################
# Optional Semicolon Production for Dangling Else Handling
#########################
def p_OptionalSemicolon(p):
    """OptionalSemicolon : ';'
                         | empty"""
    p[0] = None


def p_empty(p):
    "empty :"
    p[0] = None


#########################
# Error Handling
#########################
def find_column(input, token):
    last_newline = input.rfind('\n', 0, token.lexpos)
    if last_newline < 0:
        last_newline = -1
    return token.lexpos - last_newline


def p_error(p):
    if p:
        line = p.lexer.lexdata[:p.lexpos].count('\n') + 1
        col = find_column(p.lexer.lexdata, p)
        syntax_errors.append(
            f"Syntax error at line {line}, column {col}: unexpected token '{p.value}'"
        )
    else:
        syntax_errors.append("Syntax error: unexpected end of input!")


lexer.lineno = 1
parser = yacc.yacc()

#########################
# Main entry point: Parse input code (Debug)
#########################
code = open("../tests/SomaArray.pas", "r").read()

parser.success = True
ast = parser.parse(code, lexer=lexer)
# if parser.success:
# print("AST:", ast)
# print("Let's GO!!!")
# else:
# print("Try again!")
