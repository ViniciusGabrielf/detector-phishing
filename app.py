import streamlit as st

from phishing.analyzer import analisar_phishing


st.set_page_config(
    page_title="Detector de Phishing",
    page_icon="🛡️",
    layout="centered"
)

st.title("Detector de Phishing")

st.write(
    "Cole abaixo um e-mail, mensagem ou URL para verificar possíveis sinais de phishing."
)

texto = st.text_area(
    "Texto, e-mail ou URL para análise",
    height=250,
    placeholder="Exemplo: Urgente! Sua conta será bloqueada. Clique aqui: http://banco-login-seguranca.com"
)

if st.button("Analisar"):
    if not texto.strip():
        st.warning("Cole um texto ou URL antes de analisar.")
    else:
        resultado = analisar_phishing(texto)

        risco = resultado["risco"]
        pontuacao = resultado["pontuacao"]

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
        st.subheader("Indicadores encontrados")

        if resultado["indicadores"]:
            for indicador in resultado["indicadores"]:
                st.write(f"- {indicador}")
        else:
            st.write("Nenhum indicador suspeito encontrado.")
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