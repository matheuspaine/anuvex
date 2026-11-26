import re
import requests
from config import URL, MODELO
from models import Produto, AnaliseIA
from classifier import categoria_por_regra, perguntas_candidatas, normalizar
from prompts import montar_prompt

def analisar_produto(produto: Produto) -> AnaliseIA:
    categoria = categoria_por_regra(produto.nome)
    candidatas = perguntas_candidatas(produto)
    prompt = montar_prompt(produto, categoria, candidatas)
    resposta = requests.post(URL, json={
        "model": MODELO, "prompt": prompt, "stream": False,
        "format": AnaliseIA.model_json_schema(),
        "options": {"temperature": 0}
    }, timeout=(5, 120), allow_redirects=False)
    resposta.raise_for_status()
    if 300 <= resposta.status_code < 400:
        raise ValueError("Redirecionamento inesperado do Ollama.")
    bruto = resposta.json()["response"]
    if not isinstance(bruto, str) or len(bruto) > 12000:
        raise ValueError("Resposta da IA fora dos limites.")
    analise = AnaliseIA.model_validate_json(bruto)
    perguntas = []
    vistos = set()
    for pergunta in analise.perguntas:
        pergunta = pergunta.strip()
        chave = re.sub(r"[^a-z0-9 ]", "", normalizar(pergunta))
        if not chave or chave in vistos:
            continue
        if candidatas is not None and pergunta not in candidatas:
            continue
        vistos.add(chave)
        perguntas.append(pergunta)
    if candidatas is not None and not perguntas:
        perguntas = candidatas[:6]
    return AnaliseIA(categoria=categoria or analise.categoria, perguntas=perguntas)
