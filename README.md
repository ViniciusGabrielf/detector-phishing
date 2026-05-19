# Detector de Phishing

Projeto desenvolvido em Python com Streamlit para identificar possíveis sinais de phishing em mensagens, e-mails e URLs.

A ferramenta analisa textos e links em busca de indicadores suspeitos, como linguagem de urgência, domínios estranhos, URLs sem HTTPS, uso de encurtadores, palavras maliciosas e possível imitação de marcas conhecidas.

## Objetivo

O objetivo deste projeto é auxiliar na identificação de mensagens suspeitas que podem tentar enganar usuários para roubar dados pessoais, senhas, informações bancárias ou credenciais de acesso.

Este projeto foi desenvolvido para fins de estudo e prática em cibersegurança, análise de URLs e desenvolvimento de aplicações com Python.

## Funcionalidades

- Análise de textos, e-mails e URLs.
- Detecção de palavras e expressões comuns em golpes.
- Extração automática de URLs presentes no texto.
- Verificação de URLs que usam HTTP em vez de HTTPS.
- Detecção de domínios com muitos hífens ou números.
- Identificação de URLs muito longas.
- Detecção de encurtadores de link.
- Análise de subdomínio, domínio e extensão.
- Detecção de possível imitação de marcas conhecidas.
- Consulta em base pública de phishing.
- Classificação do risco em baixo, médio ou alto.
- Exibição dos indicadores encontrados.
- Interface web simples usando Streamlit.

## Tecnologias utilizadas

- Python
- Streamlit
- Regex
- Requests
- TLDExtract
- RapidFuzz
- Python Dotenv

## Estrutura do projeto

```txt
detector-phishing/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── brands.json
│
└── phishing/
    ├── __init__.py
    ├── analyzer.py
    ├── brand_checker.py
    ├── domain_checker.py
    ├── patterns.py
    ├── risk_score.py
    ├── text_checker.py
    ├── threat_feeds.py
    └── url_checker.py
