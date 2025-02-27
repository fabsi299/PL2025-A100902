import re
import sys
from typing import List, Tuple

# Definição de tipos de tokens
TOKEN_TYPES = [
    (r'(?i)SELECT', 'SELECT'),
    (r'(?i)WHERE', 'WHERE'),
    (r'(?i)LIMIT', 'LIMIT'),
    (r'FILTER', 'FILTER'),
    (r'PREFIX', 'PREFIX'),
    (r'(?i)a', 'TYPE'),  # Reconhece 'a' como palavra-chave
    (r'\?[a-zA-Z_:][a-zA-Z0-9_:]*', 'VARIABLE'),
    (r'([a-zA-Z_][a-zA-Z0-9_]*)\:([a-zA-Z0-9_]+)', 'DATABASE_IDENTIFIER'),  # Divide dbo:name em DATABASE e IDENTIFIER
    (r'[0-9]+', 'NUMBER'),
    (r'\.', 'DOT'),
    (r'\:', 'COLON'),
    (r',', 'COMMA'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'\{', 'LBRACE'),
    (r'\}', 'RBRACE'),
    (r'@en', 'LANG_TAG'),
    (r'"[^"]*"', 'STRING'),
    (r'<[^>]*>', 'URI'),
    (r'\s+', None)  # Ignorar espaços em branco
]


def tokenize(query: str) -> List[Tuple[str, str]]:
    """
    Tokeniza a string de entrada com base nas regras definidas.
    Retorna uma lista de tuplas (tipo, valor).
    """
    tokens = []
    while query:
        match = None
        for pattern, token_type in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(query)
            if match:
                value = match.group(0)
                if token_type:  # Ignorar tokens sem tipo (espaços, por exemplo)
                    if token_type == 'DATABASE_IDENTIFIER':
                        tokens.append(('DATABASE', match.group(1)))
                        tokens.append(('IDENTIFIER', match.group(2)))
                    else:
                        tokens.append((token_type, value))
                query = query[len(value):]  # Avança na string
                break
        if not match:
            raise SyntaxError(f"Token inválido encontrado: {query}")
    return tokens


def main():
    if len(sys.argv) != 2:
        print("Erro: Por favor, forneça o caminho do arquivo de consulta.")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as file:
            query = file.read().strip()

        tokens = tokenize(query)
        for token in tokens:
            print(token)

    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    except Exception as e:
        print(f"Erro: {str(e)}")


if __name__ == "__main__":
    main()
