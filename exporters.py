import json

def formatar_preco(preco):
    return f"{preco:,.2f}".translate(str.maketrans(",.", ".,"))

def exportar(anuncio, descricao, produto, categoria, confirmadas, nota, avisos):
    dados = {"titulo": anuncio.titulo, "descricao": descricao, "preco": float(produto.preco),
             "moeda": "BRL", "categoria": categoria, "respostas_confirmadas": confirmadas,
             "completude_percentual": nota, "avisos_consistencia": avisos}
    texto = f"{anuncio.titulo}\n\n{descricao}\n\nPreço: R$ {formatar_preco(produto.preco)}\nCategoria: {categoria}\nCompletude: {nota}%"
    if avisos:
        texto += "\n\nAlertas de revisão (não fazem parte do anúncio):\n" + "\n".join(avisos)
    return dados, texto

def exportar_json(dados):
    return json.dumps(dados, ensure_ascii=False, indent=2)
