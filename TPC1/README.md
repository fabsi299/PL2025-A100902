# TPC1 - Somador On/Off

## Autor
- Fábio Daniel Rodrigues Leite
- A100902

## Resumo

Primeiramente são inicializadas as variáveis ligado (inicialmente com valor 'False', que guarda o estado do somador) e a soma (que irá guardar o resultado das sucessivas somas).

Através do uso do módulo re, o texto é dividido nos pontos onde aparecem "On", "Off" ou "=".
A flag re.IGNORECASE permite que as palavras sejam reconhecidas independentemente de maiúsculas ou minúsculas.

Após isso é feito um loop que a cada parte do texto resultante do 're.split()' verifica o tipo dessa dada parte e caso seja:
- on : coloca a variavél 'ligado' com valor 'True'.
- off : coloca a variavél 'ligado' com valor 'False'.
- = : apresenta o valor atual da variável 'soma'.
- texto : verifica o estado do contador e, caso a variável 'ligado' esteja com valor 'True', utiliza re.findall() para ir buscar apenas os números a essa parte textual e executa a soma..