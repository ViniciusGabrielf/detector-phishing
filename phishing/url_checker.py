import re
from urllib.parse import urlparse

from .patterns import ENCURTADORES, PALAVRAS_URL_SUSPEITAS


def extrair_urls(texto):
    padrao = r"(?:https?://|www\.)[^\s]+"
    urls = re.findall(padrao, texto)

    urls_limpas = []

    for url in urls:
        url = url.strip().rstrip(".,);]}")
        urls_limpas.append(url)

    return urls_limpas


def analisar_url(url):
    pontos = 0
    indicadores = []

    url_original = url

    if url.startswith("www."):
        url = "https://" + url
        pontos += 10
        indicadores.append("A URL não informa claramente o protocolo")

    parsed = urlparse(url)
    dominio = parsed.netloc.lower()
    caminho = parsed.path.lower()

    if url_original.startswith("http://"):
        pontos += 20
        indicadores.append("A URL usa HTTP em vez de HTTPS")

    if dominio in ENCURTADORES:
        pontos += 20
        indicadores.append("A URL usa encurtador de link")

    if dominio.count("-") >= 2:
        pontos += 15
        indicadores.append("O domínio possui muitos hífens")

    quantidade_numeros = sum(char.isdigit() for char in dominio)

    if quantidade_numeros >= 3:
        pontos += 10
        indicadores.append("O domínio possui muitos números")

    if len(url_original) > 80:
        pontos += 10
        indicadores.append("A URL é muito longa")

    for palavra in PALAVRAS_URL_SUSPEITAS:
        if palavra in dominio or palavra in caminho:
            pontos += 10
            indicadores.append(f"Palavra suspeita encontrada na URL: {palavra}")

    return pontos, indicadores