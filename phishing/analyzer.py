from .brand_checker import analisar_imitacao_marca
from .domain_checker import analisar_dominio
from .risk_score import classificar_risco
from .text_checker import analisar_texto
from .threat_feeds import consultar_phishtank
from .url_checker import analisar_url, extrair_urls


def analisar_phishing(texto):
    pontos_totais = 0
    indicadores_totais = []
    detalhes_dominios = []
    suspeitas_marcas = []

    pontos_texto, indicadores_texto = analisar_texto(texto)
    pontos_totais += pontos_texto
    indicadores_totais.extend(indicadores_texto)

    urls = extrair_urls(texto)

    for url in urls:
        pontos_url, indicadores_url = analisar_url(url)
        pontos_totais += pontos_url
        indicadores_totais.extend(indicadores_url)

        pontos_dominio, indicadores_dominio, detalhes = analisar_dominio(url)
        pontos_totais += pontos_dominio
        indicadores_totais.extend(indicadores_dominio)

        if detalhes:
            detalhes_dominios.append({
                "url": url,
                **detalhes
            })

        pontos_marca, indicadores_marca, suspeitas = analisar_imitacao_marca(url)
        pontos_totais += pontos_marca
        indicadores_totais.extend(indicadores_marca)
        suspeitas_marcas.extend(suspeitas)

    pontos_feed, indicadores_feed, encontrados_feed = consultar_phishtank(urls)
    pontos_totais += pontos_feed
    indicadores_totais.extend(indicadores_feed)

    pontos_totais = min(pontos_totais, 100)
    risco = classificar_risco(pontos_totais)

    return {
        "risco": risco,
        "pontuacao": pontos_totais,
        "urls_encontradas": urls,
        "indicadores": indicadores_totais,
        "detalhes_dominios": detalhes_dominios,
        "feed_phishing": encontrados_feed,
        "suspeitas_marcas": suspeitas_marcas,
    }