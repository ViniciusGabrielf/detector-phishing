from email import policy
from email.parser import BytesParser


def ler_txt(arquivo):
    conteudo = arquivo.read()

    try:
        return conteudo.decode("utf-8")
    except UnicodeDecodeError:
        return conteudo.decode("latin-1")


def extrair_corpo_email(mensagem):
    partes_texto = []

    if mensagem.is_multipart():
        for parte in mensagem.walk():
            tipo = parte.get_content_type()

            if tipo == "text/plain":
                try:
                    partes_texto.append(parte.get_content())
                except Exception:
                    pass
    else:
        try:
            partes_texto.append(mensagem.get_content())
        except Exception:
            pass

    return "\n".join(partes_texto)


def ler_eml(arquivo):
    mensagem = BytesParser(policy=policy.default).parsebytes(arquivo.read())

    remetente = mensagem.get("From", "")
    destinatario = mensagem.get("To", "")
    assunto = mensagem.get("Subject", "")

    corpo = extrair_corpo_email(mensagem)

    texto_final = f"""
Remetente: {remetente}
Destinatário: {destinatario}
Assunto: {assunto}

{corpo}
"""

    return texto_final.strip()


def ler_arquivo_enviado(arquivo):
    nome = arquivo.name.lower()

    if nome.endswith(".eml"):
        return ler_eml(arquivo)

    if nome.endswith(".txt"):
        return ler_txt(arquivo)

    raise ValueError("Formato não suportado. Envie um arquivo .txt ou .eml.")