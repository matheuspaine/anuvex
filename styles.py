import streamlit as st

def aplicar_estilo():
    # Identidade visual do Anuvex
    st.markdown("""
    <style>
    :root {
        --anu-lilas: #9D7CFF;
        --anu-lilas-escuro: #7C3AED;
        --anu-laranja: #F59E0B;
        --anu-laranja-escuro: #EA580C;
        --anu-fundo: #1A1328;
    }
    .stApp, [data-testid="stHeader"] {
        background-color: var(--anu-fundo);
        color: #F5F5F7;
    }
    [data-testid="stMainBlockContainer"] {max-width: 850px; padding-top: 3rem;}
    .anu-brand {display:flex; align-items:center; gap:16px; margin-bottom:8px;}
    .anu-brand h1 {color:var(--anu-lilas); font-size:2.8rem; margin:0; padding:0; letter-spacing:-1.5px;}
    .anu-brand svg {flex-shrink:0;}
    .anu-slogan {color:#C7C2D6; margin:0 0 1.3rem;}
    [data-testid="stForm"] {background:#241A38; border:1px solid #4A3A67; border-radius:18px; padding:24px;}
    [data-testid="stWidgetLabel"] p {color:#E6E2F4; font-weight:500;}
    [data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {
        background:#2E2246 !important; border-color:#4A3A67 !important; color:#F5F5F7 !important;
    }
    [data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within, [data-baseweb="select"]:focus-within > div {
        border-color:var(--anu-lilas) !important; box-shadow:0 0 0 1px var(--anu-lilas-escuro);
    }
    .stApp input, .stApp textarea {background-color:#2E2246 !important; color:#F5F5F7 !important; -webkit-text-fill-color:#F5F5F7;}
    [data-testid="stNumberInput"] button {background-color:#2E2246 !important; color:#F5F5F7 !important;}
    [data-testid="stFormSubmitButton"] button {
        background:var(--anu-laranja) !important; color:#0A0A0F !important; border:1px solid var(--anu-laranja) !important;
        border-radius:10px; min-height:46px; font-weight:700; transition:background .18s ease;
    }
    [data-testid="stFormSubmitButton"] button:hover {background:var(--anu-laranja-escuro) !important; border-color:var(--anu-laranja-escuro) !important;}
    [data-testid="stFormSubmitButton"] button p {color:#0A0A0F !important; font-weight:700;}
    [data-testid="stFormSubmitButton"] button:focus-visible {outline:3px solid var(--anu-lilas); outline-offset:3px;}
    [data-testid="stMetricValue"] {color:var(--anu-lilas);}
    [data-testid="stCaptionContainer"] p {color:#C7C2D6;}
    .stApp a {color:var(--anu-lilas);}
    .stApp hr {border-color:#4A3A67;}
    [data-testid="stProgress"] [data-baseweb="progress-bar"] > div > div {
        background-color: var(--anu-lilas) !important;
    }
    [data-testid="stDownloadButton"] button {
        background: var(--anu-laranja) !important;
        color: #0A0A0F !important;
        border: 1px solid var(--anu-laranja) !important;
        border-radius: 10px;
        font-weight: 700;
    }
    [data-testid="stDownloadButton"] button p {color:#0A0A0F !important;}
    [data-testid="stDownloadButton"] button:hover {
        background: var(--anu-laranja-escuro) !important;
        border-color: var(--anu-laranja-escuro) !important;
    }
    [data-testid="stDownloadButton"] button:focus-visible {
        outline: 3px solid var(--anu-lilas); outline-offset: 3px;
    }
    /* Fundo da barra de progresso */
[data-testid="stProgress"] [role="progressbar"] {
    background-color: #392B54 !important;
}

/* Parte preenchida da barra */
[data-testid="stProgress"] [role="progressbar"] > div {
    background-color: #9D7CFF !important;
}

[data-testid="stProgress"] [role="progressbar"] > div > div {
    background-color: #9D7CFF !important;
}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="anu-brand">
    <svg width="58" height="58" viewBox="0 0 80 80" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="anuvexAGrad" x1="0%" y1="0%" x2="80%" y2="100%"><stop offset="0%" stop-color="#FFBC75"/><stop offset="45%" stop-color="#F59E0B"/><stop offset="100%" stop-color="#EA580C"/></linearGradient></defs><path fill="url(#anuvexAGrad)" fill-rule="evenodd" d="M40 5 C28 5 23 9 19 23 L5 65 Q2 75 13 75 L22 75 Q28 75 31 66 L34 57 Q35 54 40 54 L45 54 Q49 54 50 58 L53 67 Q56 75 64 75 L70 75 Q78 75 75 65 L61 23 C57 9 52 5 40 5 Z M40 27 Q42 23 44 29 L49 43 Q50 47 45 47 L35 47 Q31 47 33 42 Z"/></svg><h1>Anuvex</h1></div>
    <p class="anu-slogan">Inteligência por trás de cada anúncio.</p>
    """, unsafe_allow_html=True)
