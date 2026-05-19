import streamlit as st

from phishing.analyzer import analisar_phishing
from phishing.file_reader import ler_arquivo_enviado
from phishing.report_builder import gerar_relatorio_markdown


st.set_page_config(
    page_title="Detector de Phishing",
    page_icon="🛡️",
    layout="centered"
)

st.title("Detector de Phishing")

st.write(
    "Analise mensagens, e-mails ou URLs para identificar possíveis sinais de phishing."
)

st.divider()

st.subheader("Entrada para análise")

arquivo = st.file_uploader(
    "Envie um arquivo .txt ou .eml",
    type=["txt", "eml"]
)

texto_digitado = st.text_area(
    "Ou cole manualmente um texto, e-mail ou URL",
    height=250,
    placeholder="Exemplo: Urgente! Sua conta será bloqueada. Clique aqui: http://banco-login-seguranca.com"
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


if st.button("Analisar"):
    if not texto_para_analisar.strip():
        st.warning("Cole um texto, URL ou envie um arquivo antes de analisar.")
    else:
        resultado = analisar_phishing(texto_para_analisar)

        risco = resultado["risco"]
        pontuacao = resultado["pontuacao"]

        st.divider()
        st.subheader("Resultado da análise")

        if risco == "Alto":
            st.error(f"Risco: {risco} — Pontuação: {pontuacao}/100")
        elif risco == "Médio":
            st.warning(f"Risco: {risco} — Pontuação: {pontuacao}/100")
        else:
            st.success(f"Risco: {risco} — Pontuação: {pontuacao}/100")

        st.subheader("URLs encontradas")

        if resultado["urls_encontradas"]:
            for url in resultado["urls_encontradas"]:
                st.code(url)
        else:
            st.write("Nenhuma URL encontrada.")

        st.subheader("Detalhes dos domínios")

        if resultado["detalhes_dominios"]:
            for item in resultado["detalhes_dominios"]:
                st.write(f"URL analisada: `{item['url']}`")
                st.write(f"Domínio principal: `{item['dominio_completo']}`")
                st.write(f"Subdomínio: `{item['subdominio'] or 'nenhum'}`")
                st.write(f"Sufixo: `.{item['sufixo']}`")
                st.divider()
        else:
            st.write("Nenhum detalhe de domínio encontrado.")

        st.subheader("Possível imitação de marca")

        if resultado["suspeitas_marcas"]:
            for item in resultado["suspeitas_marcas"]:
                st.warning(f"Possível imitação da marca: {item['marca']}")
                st.write(f"Domínio analisado: `{item['dominio_analisado']}`")
                st.write(f"Domínio oficial comparado: `{item['dominio_oficial']}`")
                st.write(f"Similaridade: `{item['similaridade']:.2f}%`")
                st.divider()
        else:
            st.write("Nenhuma tentativa clara de imitação de marca foi encontrada.")

        st.subheader("Indicadores encontrados")

        if resultado["indicadores"]:
            for indicador in resultado["indicadores"]:
                st.write(f"- {indicador}")
        else:
            st.write("Nenhum indicador suspeito encontrado.")

        st.subheader("Consulta em base pública de phishing")

        if resultado["feed_phishing"]:
            for item in resultado["feed_phishing"]:
                st.error("URL encontrada em base de phishing verificado.")
                st.write(f"Alvo/empresa imitada: {item['alvo']}")
                st.write(f"Verificado: {item['verificado']}")
                st.write(f"Online: {item['online']}")
                st.write(f"Detalhes: {item['detalhe']}")
        else:
            st.write(
                "A URL não foi encontrada no feed consultado. Isso não significa que ela é segura; apenas que não houve correspondência na base usada."
            )

        st.subheader("Recomendação")

        if risco == "Alto":
            st.write(
                "Não clique no link. Verifique a informação diretamente no site oficial da empresa."
            )
        elif risco == "Médio":
            st.write(
                "Tenha cuidado. Confira o remetente, o domínio e evite informar dados pessoais."
            )
        else:
            st.write(
                "Nenhum sinal forte de phishing foi encontrado, mas continue verificando a origem da mensagem."
            )

        relatorio = gerar_relatorio_markdown(texto_para_analisar, resultado)

        st.download_button(
            label="Baixar relatório",
            data=relatorio,
            file_name="relatorio_phishing.md",
            mime="text/markdown"
        )