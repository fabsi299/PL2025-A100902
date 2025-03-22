# TPC5 - Máquinas de estados (meta-autómato)

## Autor
- Fábio Daniel Rodrigues Leite
- A100902

## Resumo

### Analisador Léxico:
Para a construção do analisador léxico foi utilizada a biblioteca PLY.lex para identificar e processar comandos como listar produtos, inserir moedas e selecionar itens, além de reconhecer códigos de produtos e valores monetários, garantindo que entradas inválidas sejam tratadas adequadamente.

### Gestão de Dados: 
Armazena e gere informações dos produtos num arquivo JSON, incluindo código, nome, quantidade e preço, garantindo que o estoque seja atualizado corretamente após cada compra e persistindo as alterações ao finalizar o programa.

### Processamento Monetário: 
Converte representações textuais de moedas (como "2e" e "50c") em valores numéricos, sendo possivel a inserção de múltiplas moedas em um único comando.
Verifica também se há saldo suficiente para compras e calcula o troco de forma eficiente utilizando as moedas disponíveis.

### Funcionalidades Implementadas
O sistema possibilita: 
- listar os produtos disponíveis com as suas respetivas informações, 
- inserir moedas para atualizar o saldo do utilizador, verificar o saldo atual, 
- selecionar um produto para compra caso haja estoque e saldo suficiente,
- finalizar a sessão calculando e devolvendo o troco corretamente.