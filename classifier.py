import re
import unicodedata
from models import Produto

def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(c for c in texto if not unicodedata.combining(c))


# Regras iniciais para produtos reconhecíveis pelo nome.
REGRAS = {
    "Informática": r"\b(teclado|mouse|notebook|computador|monitor|placa de video|rtx|ssd|impressora)\b",
    "Celulares": r"\b(iphone|celular|smartphone|galaxy s\d+|galaxy a\d+)\b",
    "Casa e decoração": r"\b(sofa|poltrona|guarda-roupa|cama|mesa de jantar|comoda)\b",
}

# Perguntas pré-definidas para os tipos já testados.
PERGUNTAS = {
    "teclado": [
        ("Qual é a marca e o modelo?", r"\b(marca|modelo|redragon|logitech|razer|corsair)\b"),
        ("Qual é a cor?", r"\b(cor|preto|preta|branco|branca|cinza|azul|rosa)\b"),
        ("Qual é o tipo de switch?", r"\b(switch|switches)\b"),
        ("Qual é o layout?", r"\b(abnt2?|ansi|iso|layout)\b"),
        ("Qual é o tipo de conexão?", r"\b(usb|bluetooth|wireless|conexao|com fio|sem fio)\b"),
        ("Possui iluminação RGB?", r"\b(rgb|iluminacao|retroiluminacao)\b"),
    ],
    "celular": [
        ("Qual é a capacidade de armazenamento?", r"\b\d+\s*(gb|tb)\b"),
        ("Qual é a cor?", r"\b(cor|preto|preta|branco|branca|cinza|azul|rosa|verde|vermelho)\b"),
        ("Qual é a saúde da bateria?", r"\b(saude da bateria|bateria\s*\d+\s*%)"),
        ("A tela apresenta riscos ou trincas?", r"\b(risco|riscos|trinca|trincas|arranhao|arranhoes)\b"),
        ("Já passou por reparos?", r"\b(reparo|reparos|conserto|consertos)\b"),
        ("Acompanha acessórios?", r"\b(acessorios|carregador|cabo|caixa)\b"),
    ],
    "sofa": [
        ("Qual é a cor?", r"\b(cor|cinza|preto|preta|branco|branca|bege|marrom|azul|verde)\b"),
        ("Quantos lugares possui?", r"\b(\d+|dois|tres|quatro|cinco)\s+lugares\b"),
        ("Qual é o material do revestimento?", r"\b(tecido|couro|suede|linho|veludo|revestimento)\b"),
        ("Quais são as dimensões?", r"\b(dimensoes|largura|altura|profundidade|\d+\s*cm)\b"),
        ("Possui manchas, rasgos ou outros danos?", r"\b(manchas?|rasgos?|danos?|avarias?)\b"),
        ("É retrátil ou reclinável?", r"\b(retratil|reclinavel)\b"),
    ],
}


def categoria_por_regra(nome: str):
    nome = normalizar(nome)
    categorias = [c for c, padrao in REGRAS.items() if re.search(padrao, nome)]
    return categorias[0] if len(categorias) == 1 else None


def perguntas_candidatas(produto: Produto):
    nome = normalizar(produto.nome)
    if re.search(r"\bteclado\b", nome):
        tipo = "teclado"
    elif categoria_por_regra(nome) == "Celulares":
        tipo = "celular"
    elif re.search(r"\bsofa\b", nome):
        tipo = "sofa"
    else:
        return None
    texto = normalizar(produto.nome + " " + produto.caracteristicas)
    return [pergunta for pergunta, padrao in PERGUNTAS[tipo]
            if not re.search(padrao, texto)]
