import re


def somador_on_off():
    texto = input("Digite o texto: ")  # Solicita entrada do usuário
    ligado = False  # Começa ligado
    soma = 0

    # Divide o texto mantendo os delimitadores ("On", "Off", "=")
    partes = re.split(r'(On|Off|=)', texto, flags=re.IGNORECASE)

    for parte in partes:
        parte = parte.strip()  # Remove espaços extras
        parte_lower = parte.lower()
        if parte_lower == "on":
            ligado = True
        elif parte_lower == "off":
            ligado = False
        elif parte == "=":
            print(soma)  # Imprime o resultado atual
        elif ligado:
            # Somar todos os números encontrados na parte
            numeros = map(int, re.findall(r'\d+', parte))
            soma += sum(numeros)

somador_on_off()