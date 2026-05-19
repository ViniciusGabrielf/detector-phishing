def gerar_relatorio_markdown(texto_analisado, resultado):
    linhas = []

    linhas.append("# Relatório de Análise de Phishing")
    linhas.append("")
    linhas.append(f"## Risco identificado")
    linhas.append("")
    linhas.append(f"- Risco: **{resultado['risco']}**")
    linhas.append(f"- Pontuação: **{resultado['pontuacao']}/100**")
    linhas.append("")

    linhas.append("## URLs encontradas")
    linhas.append("")

    if resultado["urls_encontradas"]:
        for url in resultado["urls_encontradas"]:
            linhas.append(f"- `{url}`")
    else:
        linhas.append("- Nenhuma URL encontrada.")

    linhas.append("")
    linhas.append("## Detalhes dos domínios")
    linhas.append("")

    if resultado.get("detalhes_dominios"):
        for item in resultado["detalhes_dominios"]:
            linhas.append(f"- URL analisada: `{item['url']}`")
            linhas.append(f"  - Domínio principal: `{item['dominio_completo']}`")
            linhas.append(f"  - Subdomínio: `{item['subdominio'] or 'nenhum'}`")
            linhas.append(f"  - Sufixo: `.{item['sufixo']}`")
    else:
        linhas.append("- Nenhum detalhe de domínio encontrado.")

    linhas.append("")
    linhas.append("## Possível imitação de marca")
    linhas.append("")

    if resultado.get("suspeitas_marcas"):
        for item in resultado["suspeitas_marcas"]:
            linhas.append(f"- Marca possivelmente imitada: **{item['marca']}**")
            linhas.append(f"  - Domínio analisado: `{item['dominio_analisado']}`")
            linhas.append(f"  - Domínio oficial comparado: `{item['dominio_oficial']}`")
            linhas.append(f"  - Similaridade: `{item['similaridade']:.2f}%`")
    else:
        linhas.append("- Nenhuma tentativa clara de imitação de marca encontrada.")

    linhas.append("")
    linhas.append("## Indicadores encontrados")
    linhas.append("")

    if resultado["indicadores"]:
        for indicador in resultado["indicadores"]:
            linhas.append(f"- {indicador}")
    else:
        linhas.append("- Nenhum indicador suspeito encontrado.")

    linhas.append("")
    linhas.append("## Consulta em base pública de phishing")
    linhas.append("")

    if resultado.get("feed_phishing"):
        for item in resultado["feed_phishing"]:
            linhas.append("- URL encontrada em base pública de phishing.")
            linhas.append(f"  - Alvo/empresa imitada: {item['alvo']}")
            linhas.append(f"  - Verificado: {item['verificado']}")
            linhas.append(f"  - Online: {item['online']}")
            linhas.append(f"  - Detalhes: {item['detalhe']}")
    else:
        linhas.append(
            "- A URL não foi encontrada no feed consultado. Isso não garante que ela é segura."
        )

    linhas.append("")
    linhas.append("## Texto analisado")
    linhas.append("")
    linhas.append("```txt")
    linhas.append(texto_analisado.strip())
    linhas.append("```")

    return "\n".join(linhas)