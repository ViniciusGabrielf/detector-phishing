import json
import os
import time
from pathlib import Path

import requests


CACHE_DIR = Path("data")
CACHE_FILE = CACHE_DIR / "phishtank_online_valid.json"
CACHE_TTL_SECONDS = 60 * 60


def normalizar_url(url):
    return url.strip().rstrip("/")


def cache_valido():
    if not CACHE_FILE.exists():
        return False

    idade_cache = time.time() - CACHE_FILE.stat().st_mtime
    return idade_cache < CACHE_TTL_SECONDS


def carregar_cache():
    if not CACHE_FILE.exists():
        return []

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception:
        return []


def salvar_cache(dados):
    CACHE_DIR.mkdir(exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False)


def baixar_feed_phishtank():
    chave = os.getenv("PHISHTANK_APP_KEY", "").strip()

    if chave:
        url = f"https://data.phishtank.com/data/{chave}/online-valid.json"
    else:
        url = "https://data.phishtank.com/data/online-valid.json"

    headers = {
        "User-Agent": "detector-phishing/projeto-academico"
    }

    resposta = requests.get(url, headers=headers, timeout=30)
    resposta.raise_for_status()

    return resposta.json()


def carregar_feed_phishtank():
    if cache_valido():
        return carregar_cache()

    try:
        dados = baixar_feed_phishtank()
        salvar_cache(dados)
        return dados
    except Exception:
        return carregar_cache()


def consultar_phishtank(urls):
    pontos = 0
    indicadores = []
    encontrados = []

    if not urls:
        return pontos, indicadores, encontrados

    feed = carregar_feed_phishtank()

    urls_feed = {}

    for item in feed:
        url_item = item.get("url")

        if url_item:
            urls_feed[normalizar_url(url_item)] = item

    for url in urls:
        url_normalizada = normalizar_url(url)

        if url_normalizada in urls_feed:
            item = urls_feed[url_normalizada]

            pontos += 70
            indicadores.append("A URL foi encontrada em uma base pública de phishing verificado")

            encontrados.append({
                "url": item.get("url"),
                "alvo": item.get("target"),
                "verificado": item.get("verified"),
                "online": item.get("online"),
                "detalhe": item.get("phish_detail_url"),
            })

    pontos = min(pontos, 100)

    return pontos, indicadores, encontrados