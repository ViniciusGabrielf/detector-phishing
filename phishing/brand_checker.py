import json
from pathlib import Path

import tldextract
from rapidfuzz import fuzz


BRANDS_FILE = Path("data") / "brands.json"


def carregar_marcas():
    if not BRANDS_FILE.exists():
        return []

    with open(BRANDS_FILE, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    marcas = []

    for categoria in dados.values():
        marcas.extend(categoria)

    return marcas


def obter_dominio_principal(url):
    resultado = tldextract.extract(url)
    return resultado.top_domain_under_public_suffix.lower()


def limpar_nome_dominio(dominio):
    """
    Exemplo:
    nubank-seguranca-login.com -> nubank-seguranca-login
    mercadolivre-pagamento.com.br -> mercadolivre-pagamento
    """
    resultado = tldextract.extract(dominio)
    return resultado.domain.lower()


def analisar_imitacao_marca(url):
    pontos = 0
    indicadores = []
    suspeitas = []

    dominio_completo = obter_dominio_principal(url)

    if not dominio_completo:
        return pontos, indicadores, suspeitas

    nome_dominio = limpar_nome_dominio(dominio_completo)
    marcas = carregar_marcas()

    for marca in marcas:
        nome_marca = marca["nome"]
        dominios_oficiais = [d.lower() for d in marca["dominios_oficiais"]]

        if dominio_completo in dominios_oficiais:
            continue

        for dominio_oficial in dominios_oficiais:
            nome_oficial = limpar_nome_dominio(dominio_oficial)

            similaridade = fuzz.partial_ratio(nome_dominio, nome_oficial)

            marca_no_dominio = nome_oficial in nome_dominio
            dominio_parecido = similaridade >= 80

            if marca_no_dominio or dominio_parecido:
                pontos += 25

                indicadores.append(
                    f"Possível tentativa de imitar a marca {nome_marca}"
                )

                suspeitas.append({
                    "marca": nome_marca,
                    "dominio_analisado": dominio_completo,
                    "dominio_oficial": dominio_oficial,
                    "similaridade": similaridade,
                })

                break

    pontos = min(pontos, 50)

    return pontos, indicadores, suspeitas