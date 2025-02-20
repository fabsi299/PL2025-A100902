import sys
import re


def formatar_nome(nome):
    # verifica se o nome contém uma vírgula, indicando que está no formato "Sobrenome, Nome"
    if ',' in nome:
        sobrenome, nome = nome.split(', ')
        return f"{nome} {sobrenome}"
    return nome


def ler_dataset(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        cabecalho = arquivo.readline().strip().split(';')  # lê o cabeçalho
        linhas = []
        linha_atual = ""
        dentro_de_aspas = False

        for linha in arquivo:
            linha = linha.strip()
            if linha:
                linha_atual = linha_atual + " " + linha if linha_atual else linha
                dentro_de_aspas ^= linha.count('"') % 2 == 1  # verifica se as aspas foram fechadas corretamente

                if not dentro_de_aspas:
                    valores = re.findall(r'(?:^|;)("(?:[^"]|"")*"|[^;]*)', linha_atual)
                    valores = [v.strip('"').replace('""', '"') for v in valores]

                    if 'compositor' in cabecalho:
                        index_compositor = cabecalho.index('compositor')
                        valores[index_compositor] = formatar_nome(valores[index_compositor])

                    linhas.append(dict(zip(cabecalho, valores)))  # associa os valores ao cabeçalho
                    linha_atual = ""
    return linhas


def obter_compositores(dados):
    compositores = set()  # uso de set para nao existirem dados duplicados
    for item in dados:
        compositor = item.get("compositor").strip()
        if compositor:
            compositores.add(compositor)

    return sorted(compositores)


def obras_por_periodo(dados):
    distribucao = {}

    for obra in dados:
        periodo = obra.get('periodo')
        nome = obra.get('nome')

        if periodo and nome:
            if periodo not in distribucao:
                distribucao[periodo] = []
            distribucao[periodo].append(nome)

    for periodo in distribucao:
        distribucao[periodo].sort()

    return distribucao


def contar_obras_por_periodo(dados):
    contagem = {}

    for periodo, titulos in dados.items():
        contagem[periodo] = len(titulos)

    return contagem


def exibir_menu():
    print("Escolha uma opção:")
    print("1. Exibir compositores")
    print("2. Contar o número de obras por período")
    print("3. Exibir distribuição das obras por período")
    print("4. Sair")


def main():
    if len(sys.argv) != 2:
        print("Caminho do arquivo CSV: ")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]
    dados = ler_dataset(caminho_arquivo)

    while True:
        exibir_menu()
        escolha = input("Insira a opção desejada: ")
        print("\n")

        if escolha == '1':
            compositores = obter_compositores(dados)
            print("Lista de compositores: \n")
            for compositor in compositores:
                print(f"- {compositor}")
            print("\n")

        elif escolha == '2':
            distribuicao = obras_por_periodo(dados)
            contagem = contar_obras_por_periodo(distribuicao)
            print("Número de obras por período: \n")
            for periodo, numero in contagem.items():
                print(f"{periodo}: {numero} obras")
            print("\n")

        elif escolha == '3':
            print("Distribuição de obras por período: \n")
            distribuicao = obras_por_periodo(dados)
            for periodo, titulos in distribuicao.items():
                print(f"{periodo}:")
                print('- ' + '\n- '.join(titulos))
            print("\n")

        elif escolha == '4':
            print("Saindo...\n")
            break

        else:
            print("Opção inválida.\n")


if __name__ == "__main__":
    main()
