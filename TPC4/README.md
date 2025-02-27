# TPC4 - Analisador Léxico.

## Autor
- Fábio Daniel Rodrigues Leite
- A100902

## Resumo

O script criado define vários tipos de padrões de tokens utilizando expressões regulares para processar uma consulta.
Os tipos de padrões incluem:

- Palavras-chave: Como SELECT, WHERE, LIMIT, FILTER, PREFIX, e a.
- Variáveis: Identificadores que começam com ?, como ?nome e ?desc.
- Identificadores das bases de dados: Padrões no formato dbo:name, divididos em DATABASE e IDENTIFIER.
- Números: Sequências de números (e.g., 1000).
- Símbolos: Pontuação como ponto (.), vírgula (,), parênteses ((, )), e chaves ({, }).
- Tags de Linguagem: Padrões como @en.
- Strings: Sequências entre aspas, como "Chuck Berry".
- URLs: Sequências entre < >, como `<`http://example.org`>`.
- Espaços em branco: Ignorados.

A função tokenize usa esses padrões para dividir o input de consulta em tokens. Se não encontrar uma correspondência válida, gera um erro.

