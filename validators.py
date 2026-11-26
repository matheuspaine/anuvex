import re
from classifier import normalizar

def resposta_conhecida(valor):
    return bool(valor.strip()) and normalizar(valor.strip()).rstrip(".!?") not in {"nao sei", "nao informado", "desconhecido", "ignorado", "nao se aplica", "n/a", "nao tenho informacao", "nao lembro"}

def validar_respostas(respostas):
    confirmadas = {}
    for pergunta, valor in respostas.items():
        valor = valor.strip()
        if not resposta_conhecida(valor):
            continue
        if len(valor) > 200:
            raise ValueError("Resposta deve ter até 200 caracteres.")
        if "saude da bateria" in normalizar(pergunta):
            if not re.fullmatch(r"\d{1,3}(?:[,.]\d{1,2})?\s*%?", valor):
                raise ValueError("Informe a saúde da bateria em porcentagem, de 0 a 100.")
            numero = float(valor.replace("%", "").replace(",", ".").strip())
            if not 0 <= numero <= 100:
                raise ValueError("A saúde da bateria deve estar entre 0% e 100%.")
            valor = f"{numero:g}".replace(".", ",") + "%"
        confirmadas[pergunta] = valor
    return confirmadas



def verificar_consistencia(produto, respostas):
    if normalizar(produto.estado) != "novo":
        return []
    texto = normalizar(produto.caracteristicas)
    bateria = any(float(n.replace(",", ".")) < 90 for n in re.findall(r"(?:saude da )?bateria\s*(?:de|:|em)?\s*(\d{1,3}(?:[,.]\d+)?)\s*%", texto) if float(n.replace(",", ".")) <= 100)
    reparos = bool(re.search(r"\b(?:ja passou por reparos|foi reparad[oa]|troquei a (?:tela|bateria))\b", texto)) and not bool(re.search(r"\b(?:nao|nunca)\s+(?:ja |foi |passou |troquei )", texto))
    danos = bool(re.search(r"\b(?:tela trincada|com riscos|com trincas)\b", texto)) and not bool(re.search(r"\b(?:sem|nao possui)\s+(?:riscos|trincas)", texto))
    for pergunta, valor in respostas.items():
        chave, resposta = normalizar(pergunta), normalizar(valor.strip())
        afirmativo = bool(re.match(r"^(?:sim\b|ja\b)", resposta)) and not bool(re.match(r"^ja\s+(?:nao|nunca)", resposta))
        if "saude da bateria" in chave:
            try:
                bateria |= 0 <= float(resposta.rstrip("%").replace(",", ".")) < 90
            except ValueError:
                pass
        if "reparos" in chave:
            reparos |= afirmativo
        if "riscos ou trincas" in chave:
            danos |= afirmativo
    avisos = []
    if bateria:
        avisos.append("Produto declarado novo com saúde da bateria abaixo de 90%. Confira o estado de conservação.")
    if reparos:
        avisos.append("Produto declarado novo com histórico de reparos informado. Confira o estado de conservação.")
    if danos:
        avisos.append("Produto declarado novo com riscos ou trincas informados. Confira a descrição.")
    return avisos
