import tldextract


def analisar_dominio(url):
    pontos = 0
    indicadores = []

    resultado = tldextract.extract(url)

    subdominio = resultado.subdomain
    dominio = resultado.domain
    sufixo = resultado.suffix
    dominio_completo = resultado.top_domain_under_public_suffix

    if not dominio_completo:
        return pontos, indicadores, {}

    if len(dominio) > 25:
        pontos += 10
        indicadores.append("O nome do domínio é muito longo")

    if subdominio.count(".") >= 2:
        pontos += 10
        indicadores.append("A URL possui muitos subdomínios")

    if sufixo in ["zip", "mov", "click", "top", "xyz", "tk", "ml", "ga"]:
        pontos += 15
        indicadores.append(f"O domínio usa uma extensão frequentemente abusada: .{sufixo}")

    detalhes = {
        "subdominio": subdominio,
        "dominio": dominio,
        "sufixo": sufixo,
        "dominio_completo": dominio_completo,
    }

    return pontos, indicadores, detalhes