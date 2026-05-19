from .patterns import PALAVRAS_SUSPEITAS


def analisar_texto(texto):
    pontos = 0
    indicadores = []

    texto_lower = texto.lower()

    for palavra in PALAVRAS_SUSPEITAS:
        if palavra in texto_lower:
            pontos += 10
            indicadores.append(f"Expressão suspeita encontrada: {palavra}")

    return pontos, indicadores