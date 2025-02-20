# TPC2 - Análise de um dataset de obras musicais

## Autor
- Fábio Daniel Rodrigues Leite
- A100902

## Resumo

- Primeiramente foi criada a função 'ler_dataset 'que permite percorrer o ficheiro '.csv' dado como argumento, processando-o e guardando os dados obtidos a partir do mesmo num dicionário. Nesta função é utilizado o módulo re para dar parse a cada linha, sendo criada uma função auxiliar ('formatar_nome') que permite colocar o nome de todos os autores numa forma genérica.
- Após o armazenamento dos dados ficheiro CSV em memória, já se torna possível "atacar" os problemas principais:

### 1.Listar os compositores musicais de forma ordenada:
- A função 'obter_compositores' percorre os dados, extraindo os nomes dos compositores, colocando-os num set para garantir que não haja repetição de dados.
- Esse set é retornado, sendo ordenado por ordem alfabética.

### 2. Listar os diferentes períodos com o número de obras correspondentes:
- A função 'obras_por_periodo' cria um dicionário onde a chave é o período e o valor é uma lista de nomes de obras desse período.
- Nesta função são percorridos os dados, adicionando o nome da obra à lista do período correspondente.
- Por fim, a lista de obras de cada período é ornada alfabeticamente, sendo depois retornado o dicionário final.

### 3. Listar as obras correspondentes a cada período de forma ordenada:
- A função 'contar_obras_por_periodo' aproveita-se da função 'obras_por_periodo', recebendo o dicionário de obras por período.
- Sendo assim só se torna necessário contar quantas obras existem em cada período, retornando um novo dicionário com a quantidade de obras para cada período.
