# TPC6 - Recursivo Descendente para expressões aritméticas

## Autor
- Fábio Daniel Rodrigues Leite
- A100902

## Resumo

### Analisador Léxico

A parte do Lexer do programa converte a ‘string’ de entrada em ‘tokens’ usando expressões regulares, identificando números, operadores e parênteses, ignorando espaços em branco, detetando tambem caracteres inválidos, avançando para o próximo caractere caso encontre um caractere inválido.
Foram definidos os seguintes ‘tokens’: 
- NUMBER, 
- PLUS,
- MINUS, 
- TIMES, 
- DIVIDE, 
- MOD,
- LPAREN, 
- RPAREN.

### Analisador Sintático

Já na parte do analisador sintático foram definidas regras para expressões binárias, parênteses, números e operador unário, tendo sido implementada hierarquia de operadores (parênteses > menos unário > multiplicação/divisão > adição/subtração)
O valor da expressão é calculado durante a análise sintática através das regras de produção, sendo ao mesmo tempo identificados os erros de sintaxe e feita a prevenção da divisão por zero.
Regras principais: Expressões binárias, agrupamento por parênteses, números e menos unário

### Conclusão

A integração do lexer e parser forma um sistema completo para análise e avaliação de expressões aritméticas, seguindo o padrão clássico de compiladores de duas fases.
