import json
import pytest
from models import Produto
from classifier import categoria_por_regra, perguntas_candidatas
from validators import validar_respostas, verificar_consistencia
from listing import gerar_anuncio_factual, calcular_completude, descricao_complementada
from exporters import exportar, exportar_json

P = "Qual é a saúde da bateria?"
R = "Já passou por reparos?"

def produto(estado="Novo"):
    return Produto(nome="iphone 13", estado=estado, caracteristicas="128 GB azul", preco=1000)

@pytest.mark.parametrize("nome,categoria", [("teclado", "Informática"), ("iPhone 13", "Celulares"), ("sofá", "Casa e decoração")])
def test_categoria(nome, categoria):
    assert categoria_por_regra(nome) == categoria

@pytest.mark.parametrize("valor", ["-64", "150", "abc"])
def test_bateria_invalida(valor):
    with pytest.raises(ValueError):
        validar_respostas({P: valor})

@pytest.mark.parametrize("valor,esperado", [("64", "64%"), ("0", "0%"), ("100", "100%")])
def test_bateria_valida(valor, esperado):
    assert validar_respostas({P: valor}) == {P: esperado}

def test_nao_sei():
    assert validar_respostas({P: "Não sei"}) == {}

def test_perguntas():
    assert "Qual é a capacidade de armazenamento?" not in perguntas_candidatas(produto())
    assert "Qual é a cor?" not in perguntas_candidatas(produto())

def test_completude():
    p = produto()
    assert calcular_completude(p, [P], {})[0] == 80
    assert calcular_completude(p, [P], {P: "64%"})[0] == 100

def test_consistencia():
    assert len(verificar_consistencia(produto(), {P: "64%", R: "sim"})) == 2
    assert verificar_consistencia(produto("Usado"), {P: "64%", R: "sim"}) == []

def test_exportacao():
    p = produto(); a = gerar_anuncio_factual(p); r = {P: "64%"}
    d = descricao_complementada(a, r)
    avisos = verificar_consistencia(p, r)
    dados, txt = exportar(a, d, p, "Celulares", r, 100, avisos)
    assert json.loads(exportar_json(dados)) == dados
    assert "R$ 1.000,00" in txt and "64%" in txt
    assert dados["avisos_consistencia"] == avisos
    assert "ótimo estado" not in d
