from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def limpar_texto(valor):
    """
    Evita erro com caracteres que a fonte padrão do ReportLab não suporta.
    """
    texto = str(valor) if valor is not None else ""
    return texto.encode("latin-1", "replace").decode("latin-1")


def texto_seguro(valor):
    return escape(limpar_texto(valor))


def cor_do_risco(risco):
    if risco == "Alto":
        return colors.HexColor("#B91C1C")

    if risco == "Médio":
        return colors.HexColor("#B45309")

    return colors.HexColor("#15803D")


def gerar_recomendacao(risco):
    if risco == "Alto":
        return (
            "Não clique no link. Não informe senhas, dados bancários ou códigos de verificação. "
            "Acesse o site oficial da empresa manualmente pelo navegador."
        )

    if risco == "Médio":
        return (
            "Tenha cuidado. Confira o remetente, o domínio do link e evite informar dados pessoais. "
            "Procure confirmar a mensagem por um canal oficial."
        )

    return (
        "Nenhum sinal forte de phishing foi encontrado, mas isso não garante segurança total. "
        "Continue verificando a origem da mensagem antes de clicar em links."
    )


def adicionar_titulo_secao(elementos, titulo, estilo):
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(texto_seguro(titulo), estilo))
    elementos.append(Spacer(1, 6))


def adicionar_lista(elementos, itens, estilo_normal):
    if not itens:
        elementos.append(Paragraph("- Nenhum item encontrado.", estilo_normal))
        return

    for item in itens:
        elementos.append(Paragraph(f"- {texto_seguro(item)}", estilo_normal))


def gerar_relatorio_pdf(texto_analisado, resultado):
    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
        title="Relatório de Análise de Phishing",
    )

    estilos = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "TituloPrincipal",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=16,
    )

    subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=estilos["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=8,
    )

    normal = ParagraphStyle(
        "NormalCustom",
        parent=estilos["BodyText"],
        fontSize=10,
        leading=14,
        wordWrap="CJK",
    )

    pequeno = ParagraphStyle(
        "Pequeno",
        parent=estilos["BodyText"],
        fontSize=8,
        leading=11,
        wordWrap="CJK",
    )

    codigo = ParagraphStyle(
        "Codigo",
        parent=estilos["Code"],
        fontName="Courier",
        fontSize=8,
        leading=11,
        wordWrap="CJK",
    )

    elementos = []

    risco = resultado.get("risco", "Não informado")
    pontuacao = resultado.get("pontuacao", 0)
    urls = resultado.get("urls_encontradas", [])
    indicadores = resultado.get("indicadores", [])
    detalhes_dominios = resultado.get("detalhes_dominios", [])
    suspeitas_marcas = resultado.get("suspeitas_marcas", [])
    feed_phishing = resultado.get("feed_phishing", [])

    elementos.append(Paragraph("Relatório de Análise de Phishing", titulo))

    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    elementos.append(
        Paragraph(f"Gerado em: {texto_seguro(data_atual)}", normal)
    )

    elementos.append(Spacer(1, 12))

    dados_resumo = [
        ["Risco", risco],
        ["Pontuação", f"{pontuacao}/100"],
        ["URLs encontradas", str(len(urls))],
        ["Indicadores encontrados", str(len(indicadores))],
        ["Possíveis imitações de marca", str(len(suspeitas_marcas))],
    ]

    tabela_resumo = Table(dados_resumo, colWidths=[180, 300])
    tabela_resumo.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3F4F6")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elementos.append(tabela_resumo)
    elementos.append(Spacer(1, 8))

    elementos.append(
        Paragraph(
            f"<b>Classificação final:</b> <font color='{cor_do_risco(risco).hexval()}'>"
            f"{texto_seguro(risco)}</font>",
            normal,
        )
    )

    adicionar_titulo_secao(elementos, "Recomendação", subtitulo)
    elementos.append(Paragraph(texto_seguro(gerar_recomendacao(risco)), normal))

    adicionar_titulo_secao(elementos, "URLs encontradas", subtitulo)

    if urls:
        for url in urls:
            elementos.append(Paragraph(f"- {texto_seguro(url)}", codigo))
    else:
        elementos.append(Paragraph("- Nenhuma URL encontrada.", normal))

    adicionar_titulo_secao(elementos, "Detalhes dos domínios", subtitulo)

    if detalhes_dominios:
        for item in detalhes_dominios:
            elementos.append(
                Paragraph(
                    f"<b>URL analisada:</b> {texto_seguro(item.get('url', ''))}",
                    normal,
                )
            )
            elementos.append(
                Paragraph(
                    f"Domínio principal: {texto_seguro(item.get('dominio_completo', ''))}",
                    pequeno,
                )
            )
            elementos.append(
                Paragraph(
                    f"Subdomínio: {texto_seguro(item.get('subdominio') or 'nenhum')}",
                    pequeno,
                )
            )
            elementos.append(
                Paragraph(
                    f"Sufixo: .{texto_seguro(item.get('sufixo', ''))}",
                    pequeno,
                )
            )
            elementos.append(Spacer(1, 6))
    else:
        elementos.append(Paragraph("- Nenhum detalhe de domínio encontrado.", normal))

    adicionar_titulo_secao(elementos, "Possível imitação de marca", subtitulo)

    if suspeitas_marcas:
        for item in suspeitas_marcas:
            elementos.append(
                Paragraph(
                    f"<b>Marca possivelmente imitada:</b> {texto_seguro(item.get('marca', ''))}",
                    normal,
                )
            )
            elementos.append(
                Paragraph(
                    f"Domínio analisado: {texto_seguro(item.get('dominio_analisado', ''))}",
                    pequeno,
                )
            )
            elementos.append(
                Paragraph(
                    f"Domínio oficial comparado: {texto_seguro(item.get('dominio_oficial', ''))}",
                    pequeno,
                )
            )
            elementos.append(
                Paragraph(
                    f"Similaridade: {float(item.get('similaridade', 0)):.2f}%",
                    pequeno,
                )
            )
            elementos.append(Spacer(1, 6))
    else:
        elementos.append(
            Paragraph("- Nenhuma tentativa clara de imitação de marca encontrada.", normal)
        )

    adicionar_titulo_secao(elementos, "Indicadores encontrados", subtitulo)
    adicionar_lista(elementos, indicadores, normal)

    adicionar_titulo_secao(elementos, "Consulta em base pública de phishing", subtitulo)

    if feed_phishing:
        for item in feed_phishing:
            elementos.append(Paragraph("<b>URL encontrada em base pública de phishing.</b>", normal))
            elementos.append(
                Paragraph(
                    f"Alvo/empresa imitada: {texto_seguro(item.get('alvo', ''))}",
                    pequeno,
                )
            )
            elementos.append(
                Paragraph(
                    f"Verificado: {texto_seguro(item.get('verificado', ''))}",
                    pequeno,
                )
            )
            elementos.append(
                Paragraph(
                    f"Online: {texto_seguro(item.get('online', ''))}",
                    pequeno,
                )
            )
            elementos.append(
                Paragraph(
                    f"Detalhes: {texto_seguro(item.get('detalhe', ''))}",
                    pequeno,
                )
            )
            elementos.append(Spacer(1, 6))
    else:
        elementos.append(
            Paragraph(
                "A URL não foi encontrada no feed consultado. Isso não garante que ela é segura.",
                normal,
            )
        )

    elementos.append(PageBreak())

    adicionar_titulo_secao(elementos, "Texto analisado", subtitulo)

    texto_formatado = texto_seguro(texto_analisado).replace("\n", "<br/>")
    elementos.append(Paragraph(texto_formatado, codigo))

    adicionar_titulo_secao(elementos, "Aviso", subtitulo)
    elementos.append(
        Paragraph(
            "Este relatório é gerado automaticamente com base em regras, padrões e consultas externas. "
            "O resultado deve ser usado como apoio para análise, não como garantia absoluta de segurança.",
            normal,
        )
    )

    documento.build(elementos)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf