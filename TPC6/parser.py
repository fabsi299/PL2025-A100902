import ply.lex as lex
import ply.yacc as yacc

# ------ Analisador Léxico (Lex) ------

# Lista de nomes de tokens
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Regras para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Ignorar espaços e tabs
t_ignore = ' \t'


# Regra para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal: '{t.value[0]}'")
    t.lexer.skip(1)


# Construir o lexer
lexer = lex.lex()

# ------ Analisador Sintático (Yacc) ------

# Definição da precedência dos operadores (do menor para o maior)
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),  # Menos unário tem maior precedência que operadores binários
)


# Regras de produção da gramática
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]  # Esta é uma subtração normal
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] == 0:
            raise ZeroDivisionError("Divisão por zero")
        p[0] = p[1] / p[3]


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]  # Menos unário - inverte o sinal


# Tratamento de erros de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe no token: '{p.value}'")
    else:
        print("Erro de sintaxe: fim inesperado da entrada")


# Construir o parser
parser = yacc.yacc()


# Função para calcular expressões
def calculate_expression(expression):
    try:
        result = parser.parse(expression, lexer=lexer)
        return result
    except ZeroDivisionError as e:
        return f"Erro: {e}"
    except Exception as e:
        return f"Erro: {e}"


# Função para testar expressões específicas
def test_specific_expressions():
    test_expressions = [
        "-1-2",  # Deve ser -3 (menos unário 1, menos binário 2)
        "-1--2",  # Deve ser 1 (menos unário 1, menos binário, menos unário 2)
    ]

    print("Teste de expressões específicas:")
    for expr in test_expressions:
        result = calculate_expression(expr)
        print(f"{expr} = {result}")

    print("-" * 50)


# Função principal com entrada do terminal
if __name__ == "__main__":
    # Testar primeiro as expressões problemáticas
    test_specific_expressions()

    print("Calculadora de Expressões Aritméticas")
    print("Digite 'sair' para encerrar")
    print("Exemplos de expressões válidas: 2+3, 67-(2+3*4), (9-2)*(13-4)")
    print("-" * 50)

    while True:
        try:
            # Receber entrada do usuário
            expression = input("Digite uma expressão: ")

            # Verificar se o usuário quer sair
            if expression.lower() in ('sair', 'exit', 'quit', 'q'):
                print("Encerrando o programa...")
                break

            # Calcular e exibir o resultado
            if expression.strip():  # Verifica se a expressão não está vazia
                result = calculate_expression(expression)
                print(f"Resultado: {result}")

        except KeyboardInterrupt:
            print("\nPrograma interrompido pelo usuário.")
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")