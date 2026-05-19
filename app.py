import streamlit as st

from phishing.analyzer import analisar_phishing
from phishing.file_reader import ler_arquivo_enviado
from phishing.report_builder import gerar_relatorio_markdown
from phishing.pdf_report import gerar_relatorio_pdf


st.set_page_config(
    page_title="Detector de Phishing",
    page_icon="🛡️",
    layout="wide"
)


def exibir_card(titulo, valor, descricao=None):
    with st.container(border=True):
        st.markdown(f"### {titulo}")
        st.markdown(f"## {valor}")
        if descricao:
            st.caption(descricao)


def exibir_resultado_risco(risco, pontuacao):
    if risco == "Alto":
        st.error(f"Risco: {risco} — Pontuação: {pontuacao}/100")
    elif risco == "Médio":
        st.warning(f"Risco: {risco} — Pontuação: {pontuacao}/100")
    else:
        st.success(f"Risco: {risco} — Pontuação: {pontuacao}/100")

    st.progress(pontuacao / 100)


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


st.title("Detector de Phishing")
st.write(
    "Analise mensagens, e-mails ou URLs para identificar possíveis sinais de phishing."
)

st.divider()

with st.sidebar:
    st.header("Sobre o projeto")
    st.write(
        "Esta ferramenta utiliza regras de análise, verificação de domínio, comparação com marcas conhecidas "
        "e consulta em base pública para estimar o risco de phishing."
    )

    st.warning(
        "A análise não garante que uma URL seja totalmente segura ou maliciosa. "
        "Use o resultado como apoio para investigação."
    )

    st.subheader("Formatos aceitos")
    st.write("- Texto manual")
    st.write("- URL")
    st.write("- Arquivo .txt")
    st.write("- Arquivo .eml")


st.subheader("Entrada para análise")

col_entrada_1, col_entrada_2 = st.columns([1, 1])

with col_entrada_1:
    arquivo = st.file_uploader(
        "Envie um arquivo .txt ou .eml",
        type=["txt", "eml"]
    )

with col_entrada_2:
    texto_digitado = st.text_area(
        "Ou cole manualmente um texto, e-mail ou URL",
        height=220,
        placeholder=(
            "Exemplo: Urgente! Sua conta será bloqueada. "
            "Clique aqui: http://banco-login-seguranca.com"
        )
    )


texto_para_analisar = ""

if arquivo is not None:
    try:
        texto_para_analisar = ler_arquivo_enviado(arquivo)
        st.success(f"Arquivo carregado: {arquivo.name}")

        with st.expander("Ver conteúdo extraído do arquivo"):
            st.text(texto_para_analisar)

    except ValueError as erro:
        st.error(str(erro))
else:
    texto_para_analisar = texto_digitado


analisar = st.button("Analisar", type="primary", use_container_width=True)

if analisar:
    if not texto_para_analisar.strip():
        st.warning("Cole um texto, URL ou envie um arquivo antes de analisar.")
    else:
        with st.spinner("Analisando conteúdo..."):
            resultado = analisar_phishing(texto_para_analisar)

        risco = resultado["risco"]
        pontuacao = resultado["pontuacao"]
        urls = resultado.get("urls_encontradas", [])
        indicadores = resultado.get("indicadores", [])
        detalhes_dominios = resultado.get("detalhes_dominios", [])
        suspeitas_marcas = resultado.get("suspeitas_marcas", [])
        feed_phishing = resultado.get("feed_phishing", [])

        st.divider()
        st.subheader("Resultado da análise")

        exibir_resultado_risco(risco, pontuacao)

        col_1, col_2, col_3, col_4 = st.columns(4)

        with col_1:
            exibir_card("Risco", risco, "Classificação final")

        with col_2:
            exibir_card("Pontuação", f"{pontuacao}/100", "Score calculado")

        with col_3:
            exibir_card("URLs", len(urls), "Links encontrados")

        with col_4:
            exibir_card("Indicadores", len(indicadores), "Sinais suspeitos")

        aba_resumo, aba_urls, aba_marcas, aba_indicadores, aba_relatorio = st.tabs(
            [
                "Resumo",
                "URLs e domínios",
                "Marcas",
                "Indicadores",
                "Relatório",
            ]
        )

        with aba_resumo:
            st.subheader("Resumo da análise")

            st.write(f"**Risco identificado:** {risco}")
            st.write(f"**Pontuação:** {pontuacao}/100")
            st.write(f"**Quantidade de URLs encontradas:** {len(urls)}")
            st.write(f"**Quantidade de indicadores:** {len(indicadores)}")

            st.subheader("Recomendação")
            st.info(gerar_recomendacao(risco))

            if feed_phishing:
                st.error(
                    "Atenção: uma ou mais URLs foram encontradas em uma base pública de phishing."
                )
            elif risco == "Alto":
                st.warning(
                    "Mesmo sem correspondência na base pública, o conteúdo possui sinais fortes de risco."
                )
            else:
                st.success(
                    "Nenhuma correspondência direta em base pública foi encontrada."
                )

        with aba_urls:
            st.subheader("URLs encontradas")

            if urls:
                for url in urls:
                    st.code(url)
            else:
                st.write("Nenhuma URL encontrada.")

            st.subheader("Detalhes dos domínios")

            if detalhes_dominios:
                for item in detalhes_dominios:
                    with st.container(border=True):
                        st.write(f"**URL analisada:** `{item['url']}`")
                        st.write(f"**Domínio principal:** `{item['dominio_completo']}`")
                        st.write(f"**Subdomínio:** `{item['subdominio'] or 'nenhum'}`")
                        st.write(f"**Sufixo:** `.{item['sufixo']}`")
            else:
                st.write("Nenhum detalhe de domínio encontrado.")

            st.subheader("Consulta em base pública de phishing")

            if feed_phishing:
                for item in feed_phishing:
                    with st.container(border=True):
                        st.error("URL encontrada em base de phishing verificado.")
                        st.write(f"**Alvo/empresa imitada:** {item['alvo']}")
                        st.write(f"**Verificado:** {item['verificado']}")
                        st.write(f"**Online:** {item['online']}")
                        st.write(f"**Detalhes:** {item['detalhe']}")
            else:
                st.write(
                    "A URL não foi encontrada no feed consultado. "
                    "Isso não significa que ela é segura; apenas que não houve correspondência na base usada."
                )

        with aba_marcas:
            st.subheader("Possível imitação de marca")

            if suspeitas_marcas:
                for item in suspeitas_marcas:
                    with st.container(border=True):
                        st.warning(f"Possível imitação da marca: {item['marca']}")
                        st.write(f"**Domínio analisado:** `{item['dominio_analisado']}`")
                        st.write(f"**Domínio oficial comparado:** `{item['dominio_oficial']}`")
                        st.write(f"**Similaridade:** `{item['similaridade']:.2f}%`")
            else:
                st.write("Nenhuma tentativa clara de imitação de marca foi encontrada.")

        with aba_indicadores:
            st.subheader("Indicadores encontrados")

            if indicadores:
                for indicador in indicadores:
                    st.write(f"- {indicador}")
            else:
                st.write("Nenhum indicador suspeito encontrado.")

        with aba_relatorio:
            st.subheader("Relatório da análise")

            relatorio_markdown = gerar_relatorio_markdown(texto_para_analisar, resultado)
            relatorio_pdf = gerar_relatorio_pdf(texto_para_analisar, resultado)

            col_pdf, col_md = st.columns(2)

            with col_pdf:
                st.download_button(
                    label="Baixar relatório em PDF",
                    data=relatorio_pdf,
                    file_name="relatorio_phishing.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            with col_md:
                st.download_button(
                    label="Baixar relatório em Markdown",
                    data=relatorio_markdown,
                    file_name="relatorio_phishing.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            with st.expander("Pré-visualizar relatório em Markdown"):
                st.markdown(relatorio_markdown)