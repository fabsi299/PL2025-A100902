import re
import json
import ply.lex as lex
from datetime import datetime

# Definição dos tokens para análise lexical
tokens = (
    'LISTAR',  # Comando para listar produtos
    'MOEDA',  # Comando para inserir moeda
    'DINHEIRO',  # Representação de valores em dinheiro
    'SELECIONAR',  # Comando para selecionar produto
    'PRODUTO',  # Código do produto
    'VIRGULA',  # Vírgula para separar valores
    'PONTO',  # Ponto para mostrar saldo
    'SAIR'  # Comando para sair
)


def t_LISTAR(t):
    r"""LISTAR|listar"""
    t.value = t.value.upper()
    return t


def t_MOEDA(t):
    r"""MOEDA|moeda"""
    t.value = t.value.upper()
    return t


def t_SELECIONAR(t):
    r"""SELECIONAR|selecionar"""
    t.value = t.value.upper()
    return t


def t_SAIR(t):
    r"""SAIR|sair"""
    t.value = t.value.upper()
    return t


t_PRODUTO = r'[A-Z]\d{2}'

t_DINHEIRO = r'\d{1,2}[ec](,\d{1,2}[ec])*'

t_VIRGULA = r','

t_PONTO = r'\.'

# Ignorar espaços e tabulações
t_ignore = " \t"


# Função para tratar erros lexicais
def t_error(t):
    print("Caractere ilegal '%s'" % t.value[0])
    t.lexer.skip(1)


# Função para tratar comandos não suportados
def t_error_command(t):
    r"""[a-zA-Z]{2,}"""
    print("Comando não suportado '%s'" % t.value)
    t.lexer.skip(1)


# Inicializar o lexer
lexer = lex.lex()

moedas = [("2e", 2.00), ("1e", 1.00), ("50c", 0.50), ("20c", 0.20), ("10c", 0.10), ("5c", 0.05), ("2c", 0.02),
          ("1c", 0.01)]


def carregar_dados_json():
    with open('stock.json', 'r', encoding='utf-8') as stock:
        return json.load(stock)


def salvar_dados_json(data):
    with open('stock.json', 'w') as stock_json:
        json.dump(data, stock_json, indent=4)


def moeda_to_num(d):
    for (m, n) in moedas:
        if m == d:
            return round(n, 2)
    return None


# Converter número para moeda
def num_to_moeda(d):
    inteiro, decimal = str("{:.2f}".format(d)).split('.')
    if int(inteiro) == 0:
        return f"{decimal}c"
    return f"{inteiro}e{decimal}c"


def listar_produtos(bd):
    print(f"{'cod':<10} | {'nome':<20} | {'quantidade':<10} | {'preço':<10}")
    print('-' * 60)
    for p in bd:
        print(f"{p['cod']:<10} | {p['nome']:<20} | {p['quant']:<10} | {p['preco']:<10.2f}")


def processar_moeda(comando, saldo_atual):
    saldo = saldo_atual
    moedas = re.findall(r'\d{1,2}[ec]', comando)  # Encontrar todas as moedas na entrada
    for moeda in moedas:
        saldo += moeda_to_num(moeda)
    return saldo


def selecionar_produto(bd, saldo):
    id_produto = lex.token().value
    produto_encontrado = False
    for prod in bd:
        if prod['cod'] == id_produto:
            produto_encontrado = True
            if prod['preco'] <= saldo:
                if prod['quant'] > 0:
                    saldo = saldo - prod['preco']
                    prod['quant'] -= 1
                    print(f"Pode retirar o produto dispensado \"{prod['nome']}\"\nSaldo: {num_to_moeda(saldo)}")
                else:
                    print("Produto sem stock")
            else:
                print(f"Saldo insuficiente para satisfazer o seu pedido\nSaldo = {num_to_moeda(saldo)}; Pedido = {num_to_moeda(prod['preco'])}")
    if not produto_encontrado:
        print("Produto não encontrado")
    return saldo


def calcular_troco(saldo):
    troco = []
    for moeda, valor in moedas:
        quantidade = int(saldo // valor)
        if quantidade > 0:
            troco.append(f"{quantidade}x {moeda}")
            saldo = round(saldo - quantidade * valor, 2)
    if len(troco) > 1:
        return ', '.join(troco[:-1]) + ' e ' + troco[-1]
    return ', '.join(troco)


def main():
    saldo = 0
    bd = carregar_dados_json()
    status = True

    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%Y-%m-%d")
    print(f"{data_formatada}, Stock carregado, Estado atualizado.")
    print(f"Bom dia. Estou disponível para atender o seu pedido.")

    while status:
        comando = input('>> ')
        lexer.input(comando)
        tok = lexer.token()
        while tok is not None:
            if tok.type == "MOEDA":
                saldo = processar_moeda(comando, saldo)
            elif tok.type == "PONTO":
                print(f"Saldo atual: {num_to_moeda(saldo)}")
            elif tok.type == "LISTAR":
                listar_produtos(bd)
            elif tok.type == "SELECIONAR":
                saldo = selecionar_produto(bd, saldo)
            elif tok.type == "SAIR":
                if saldo >= 0:
                    print(f"Pode retirar o troco: {calcular_troco(saldo)}")
                    print(f"Até à próxima!")
                saldo = 0
                status = False
            tok = lexer.token()
    salvar_dados_json(bd)


if __name__ == "__main__":
    main()
