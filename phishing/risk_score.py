def classificar_risco(pontos):
    if pontos >= 70:
        return "Alto"
    elif pontos >= 35:
        return "Médio"

    return "Baixo"