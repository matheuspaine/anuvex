import re
from models import Produto, Anuncio
from validators import resposta_conhecida

def gerar_anuncio_factual(produto: Produto) -> Anuncio:
    """Melhora a apresentação sem adicionar fatos ao conteúdo informado."""
    nome = re.sub(r"\biphone\b", "iPhone", produto.nome, flags=re.I)
    if not nome.startswith("iPhone"):
        nome = nome[0].upper() + nome[1:]
    titulo = f"{nome} — {produto.estado}"
    descricao = f"{nome} à venda. Estado de conservação: {produto.estado.lower()}."
    if produto.caracteristicas:
        descricao += f" Características informadas: {produto.caracteristicas.rstrip('.')}."
    return Anuncio(titulo=titulo, descricao=descricao)


def rotulo(pergunta):
    mapa = {
        "Qual é a saúde da bateria?": "Saúde da bateria",
        "Acompanha acessórios?": "Acompanha acessórios",
        "A tela apresenta riscos ou trincas?": "Riscos ou trincas na tela",
        "Já passou por reparos?": "Histórico de reparos",
        "Qual é a capacidade de armazenamento?": "Armazenamento",
        "Qual é a cor?": "Cor",
    }
    return mapa.get(pergunta, pergunta.rstrip("?"))


def calcular_completude(produto, perguntas, confirmadas):
    criterios = [("Nome do produto", bool(produto.nome)),
                 ("Estado de conservação", bool(produto.estado)),
                 ("Preço", produto.preco > 0),
                 ("Características", resposta_conhecida(produto.caracteristicas))]
    criterios.extend((rotulo(p), resposta_conhecida(confirmadas.get(p, ""))) for p in dict.fromkeys(perguntas))
    return round(100 * sum(ok for _, ok in criterios) / len(criterios)), criterios



def descricao_complementada(anuncio, confirmadas):
    descricao = anuncio.descricao
    if confirmadas:
        descricao += "\n\nInformações complementares:\n" + "\n".join(f"• {rotulo(p)}: {r}" for p, r in confirmadas.items())
    return descricao
