import streamlit as st
import requests
from pydantic import ValidationError
from models import Produto
from config import CATEGORIAS
from classifier import categoria_por_regra, perguntas_candidatas, normalizar
from ai_service import analisar_produto
from validators import validar_respostas, verificar_consistencia, resposta_conhecida
from listing import gerar_anuncio_factual, descricao_complementada, calcular_completude
from exporters import formatar_preco, exportar, exportar_json
from styles import aplicar_estilo

st.set_page_config(
    page_title="Anuvex",
    page_icon="⚡",
    layout="centered"
)

aplicar_estilo()

st.write("Assistente inteligente de anúncios para marketplaces.")
st.divider()

with st.form("formulario_produto"):
    nome = st.text_input("Nome do produto")
    estado = st.selectbox(
        "Estado de conservação",
        ["Novo", "Seminovo", "Usado"]
    )
    caracteristicas = st.text_area("Características", max_chars=500)
    preco = st.number_input(
        "Preço (R$)", min_value=0.0, step=1.0, format="%.2f"
    )
    gerar = st.form_submit_button(
        "✦ Gerar anúncio", use_container_width=True
    )

if gerar:
    st.session_state.pop("resultado_anuvex", None)
    st.session_state.pop("complementos_anuvex", None)
    st.session_state["geracao_anuvex"] = st.session_state.get("geracao_anuvex", 0) + 1
    try:
        produto = Produto(nome=nome.strip(), estado=estado,
                          caracteristicas=caracteristicas.strip(), preco=preco)
        anuncio = gerar_anuncio_factual(produto)
        analise = None
        aviso = None
        try:
            with st.spinner("Analisando categoria e informações com IA..."):
                analise = analisar_produto(produto)
        except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
            aviso = "Não foi possível obter a análise da IA. O anúncio factual continua disponível."
        st.session_state["resultado_anuvex"] = (produto, anuncio, analise, aviso)
    except ValidationError as erro:
        st.error("Verifique os dados informados.")
        st.text(str(erro))

if "resultado_anuvex" in st.session_state:
    produto, anuncio, analise, aviso = st.session_state["resultado_anuvex"]
    geracao = st.session_state.get("geracao_anuvex", 0)
    categorias = CATEGORIAS
    categoria_inicial = categoria_por_regra(produto.nome) or (analise.categoria if analise else "Outros")
    candidatas = perguntas_candidatas(produto)
    perguntas = candidatas if candidatas is not None else (analise.perguntas if analise else [])
    anteriores = st.session_state.get("complementos_anuvex", {})
    if aviso:
        st.warning(aviso)
    st.subheader("Complemente seu anúncio")
    st.caption("Confirme a categoria e responda apenas ao que souber. As respostas são opcionais.")
    with st.form(f"complementos_{geracao}"):
        categoria = st.selectbox("Categoria (pode corrigir)", categorias,
                                 index=categorias.index(anteriores.get("categoria", categoria_inicial)))
        respostas = {}
        for i, pergunta in enumerate(perguntas):
            respostas[pergunta] = st.text_input(pergunta, max_chars=200,
                value=anteriores.get("respostas", {}).get(pergunta, ""),
                key=f"resposta_{geracao}_{i}").strip()
        atualizar = st.form_submit_button("Atualizar anúncio")
    if atualizar:
        try:
            anteriores = {"categoria": categoria, "respostas": validar_respostas(respostas)}
            st.session_state["complementos_anuvex"] = anteriores
        except ValueError as erro:
            st.error(str(erro))
            st.info("O anúncio anterior foi mantido. Corrija a resposta e atualize novamente.")
    categoria_final = anteriores.get("categoria", categoria_inicial)
    confirmadas = {p: r for p, r in anteriores.get("respostas", {}).items()
                   if resposta_conhecida(r)}
    descricao_final = descricao_complementada(anuncio, confirmadas)
    preco_formatado = formatar_preco(produto.preco)
    st.divider()
    st.success("Anúncio montado com os dados informados!")
    st.subheader(anuncio.titulo)
    st.text(descricao_final)
    st.metric("Preço", f"R$ {preco_formatado}")
    st.text(f"Categoria: {categoria_final}")
    st.warning("Revise as informações antes de publicar.")
    st.subheader("Completude do anúncio")
    perguntas_avaliacao = perguntas_candidatas(produto)
    if perguntas_avaliacao is None:
        perguntas_avaliacao = perguntas
    nota, criterios = calcular_completude(produto, perguntas_avaliacao, confirmadas)
    st.metric("Campos preenchidos", f"{nota}%")
    st.progress(nota / 100)
    st.caption("Indicador de preenchimento dos campos avaliados, não de veracidade ou qualidade comercial.")
    if not analise and perguntas_candidatas(produto) is None:
        st.caption("Sem análise de IA: apenas os campos básicos foram avaliados.")
    for campo, ok in criterios:
        st.text(("✓ " if ok else "○ ") + campo)

    avisos = verificar_consistencia(produto, confirmadas)
    st.subheader("Análise de consistência")
    if avisos:
        for alerta in avisos:
            st.warning(alerta)
    else:
        st.caption("Nenhum alerta nas regras avaliadas. Isso não comprova a veracidade do anúncio.")
    exportacao, texto = exportar(anuncio, descricao_final, produto, categoria_final, confirmadas, nota, avisos)
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Baixar TXT", texto, "anuvex-anuncio.txt", "text/plain")
    with col2:
        st.download_button("Baixar JSON", exportar_json(exportacao),
                           "anuvex-anuncio.json", "application/json")
    with st.expander("Visualizar resposta JSON"):
        st.json(exportacao)

st.divider()
st.caption("Anuvex | Projeto educacional independente | Python, Streamlit, Ollama e Qwen")
