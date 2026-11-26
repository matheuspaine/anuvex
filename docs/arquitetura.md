# Arquitetura do Anuvex 4.2

O diagrama representa o fluxo lógico, não uma infraestrutura AWS implantada.

```mermaid
sequenceDiagram
    actor V as Vendedor
    participant A as Streamlit / app.py
    participant M as models.py
    participant C as classifier.py
    participant S as ai_service.py
    participant O as Ollama local
    participant L as listing.py / validators.py
    participant E as exporters.py
    V->>A: Dados do produto
    A->>M: Validar entrada
    A->>L: Montar anúncio factual
    A->>S: Solicitar análise
    S->>C: Categoria e perguntas candidatas
    S->>O: POST /api/generate (JSON schema)
    O-->>S: Sugestões estruturadas
    S-->>A: Resultado validado ou falha tratada
    A->>C: Regras locais e fallback
    A-->>V: Categoria e perguntas
    V->>A: Confirmar respostas e categoria
    A->>L: Validar, calcular completude e alertas
    A->>E: Montar TXT e JSON
    E-->>V: Arquivos para download
```

## Fronteiras e decisões

O Streamlit escuta em 127.0.0.1:8501 e o Ollama em localhost:11434. O modelo recebe dados do produto e retorna sugestões, não o texto final. Para teclado, celular e sofá, a interface utiliza perguntas candidatas determinísticas; para demais tipos pode utilizar as sugestões validadas do modelo. O estado da sessão mantém as respostas durante a interação, sem banco de dados persistente. Em falhas da API, o anúncio factual permanece disponível; a classificação local ou a categoria Outros é usada. A revisão humana é necessária antes de publicação externa.
