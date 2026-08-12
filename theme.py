# -*- coding: utf-8 -*-
"""
theme.py
─────────────────────────────────────────────────────────────────────────────
Estilo visual dark (IBM Plex) + helpers HTML/CSS para o app Streamlit.

Exporta:
  • Constantes de cores (VERDE, AMARELO, LARANJA, VERM, AZUL, BG, BG2, BORDER, TXT)
  • COR_CAT — cores por categoria fuzzy
  • inject_css() — CSS global injetado no app
  • plotly_dark(fig, height) — aplica tema dark a qualquer figura Plotly
  • badge(texto) / theory(html) / success(html) / warning(html) — blocos visuais
  • metric_card(titulo, valor, subtitulo) — card de métricas estilizado
  • cat_pill(categoria) — pill colorido inline para nome de categoria
  • formula(html) — bloco de fórmula destacado
"""

# ─────────────────────────────────────────────────────────────────────────────
# Paleta de cores
# ─────────────────────────────────────────────────────────────────────────────
VERDE    = "#4ade80"
AMARELO  = "#fbbf24"
LARANJA  = "#fb923c"
VERM     = "#ef4444"
AZUL     = "#4fc3f7"
ROXO     = "#a78bfa"
BRANCO   = "#f0f0f0"

# Backgrounds e bordas
BG       = "#0e1117"      # fundo principal (Streamlit dark)
BG2      = "#161b22"      # fundo secundário (cards, painéis)
BG3      = "#1c2333"      # fundo terciário (hover)
BORDER   = "#30363d"      # borda sutil
TXT      = "#e6edf3"      # texto principal
TXT2     = "#8b949e"      # texto secundário

# Mapeamento categoria → cor
COR_CAT = {
    "Baixo":    VERDE,
    "Moderado": AMARELO,
    "Alto":     LARANJA,
    "Crítico":  VERM,
}


# ─────────────────────────────────────────────────────────────────────────────
# CSS global
# ─────────────────────────────────────────────────────────────────────────────
def inject_css():
    """Retorna bloco <style> com o CSS global do app."""
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    /* ── Forçar tema dark globalmente ─────────────────────────── */
    html, body, [class*="st-"] {{
        font-family: 'IBM Plex Sans', sans-serif;
    }}

    .stApp, .stApp > header, .stApp [data-testid="stAppViewContainer"],
    .stApp [data-testid="stVerticalBlock"],
    .stApp [data-testid="stMain"],
    .stApp .main .block-container {{
        background-color: {BG} !important;
        color: {TXT} !important;
    }}

    /* Textos do Streamlit — forçar cor clara */
    .stApp p, .stApp li, .stApp span, .stApp div,
    .stApp label, .stApp .stMarkdown, .stApp h1, .stApp h2,
    .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stMarkdownContainer"] li,
    .stApp [data-testid="stCaptionContainer"] {{
        color: {TXT} !important;
    }}

    .stApp [data-testid="stCaptionContainer"] p,
    .stApp [data-testid="stCaptionContainer"] span {{
        color: {TXT2} !important;
    }}

    code, pre, .stCode {{
        font-family: 'IBM Plex Mono', monospace !important;
    }}

    /* ── Metric cards ─────────────────────────────────────────── */
    .metric-card {{
        background: linear-gradient(135deg, {BG2} 0%, {BG3} 100%) !important;
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        text-align: center;
        transition: transform 0.15s ease, box-shadow 0.2s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    }}
    .metric-card .mc-title {{
        font-size: 0.78rem;
        font-weight: 500;
        color: {TXT2} !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.3rem;
    }}
    .metric-card .mc-value {{
        font-size: 1.6rem;
        font-weight: 700;
        color: {AZUL} !important;
        line-height: 1.2;
    }}
    .metric-card .mc-sub {{
        font-size: 0.72rem;
        color: {TXT2} !important;
        margin-top: 0.25rem;
    }}

    /* ── Theory box ───────────────────────────────────────────── */
    .theory-box {{
        background: {BG2} !important;
        border-left: 4px solid {AZUL};
        border: 1px solid {BORDER};
        border-left: 4px solid {AZUL};
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.3rem;
        margin: 0.8rem 0 1.2rem 0;
        font-size: 0.92rem;
        line-height: 1.6;
        color: {TXT} !important;
    }}
    .theory-box b, .theory-box i, .theory-box span {{
        color: {TXT} !important;
    }}

    /* ── Success box ──────────────────────────────────────────── */
    .success-box {{
        background: {BG2} !important;
        border: 1px solid {BORDER};
        border-left: 4px solid {VERDE};
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.3rem;
        margin: 0.8rem 0 1.2rem 0;
        font-size: 0.92rem;
        line-height: 1.6;
        color: {TXT} !important;
    }}
    .success-box b, .success-box i, .success-box span {{
        color: {TXT} !important;
    }}

    /* ── Warning box ──────────────────────────────────────────── */
    .warning-box {{
        background: {BG2} !important;
        border: 1px solid {BORDER};
        border-left: 4px solid {AMARELO};
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.3rem;
        margin: 0.8rem 0 1.2rem 0;
        font-size: 0.92rem;
        line-height: 1.6;
        color: {TXT} !important;
    }}
    .warning-box b, .warning-box i, .warning-box span {{
        color: {TXT} !important;
    }}

    /* ── Badge pill ───────────────────────────────────────────── */
    .badge {{
        display: inline-block;
        background: linear-gradient(135deg, {AZUL}, {ROXO}) !important;
        color: {BG} !important;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }}

    /* ── Category pills (inline) ──────────────────────────────── */
    .cat-pill {{
        display: inline-block;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.15rem 0.6rem;
        border-radius: 12px;
        margin: 0 0.15rem;
        font-family: 'IBM Plex Mono', monospace;
    }}

    /* ── Formula block ────────────────────────────────────────── */
    .formula-box {{
        background: {BG2} !important;
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 0.9rem 1.3rem;
        text-align: center;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1rem;
        color: {AZUL} !important;
        margin: 0.6rem 0;
    }}

    /* ── Rule firing display ──────────────────────────────────── */
    .rule-fire {{
        background: {BG2} !important;
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 0.5rem 0.9rem;
        margin: 0.3rem 0;
        font-size: 0.88rem;
        font-family: 'IBM Plex Mono', monospace;
        line-height: 1.7;
        color: {TXT} !important;
    }}

    /* ── Sidebar tweaks ───────────────────────────────────────── */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {BG} 0%, {BG2} 100%) !important;
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {{
        color: {TXT} !important;
    }}

    /* Fallback for environments where Streamlit's Material Symbols font is
       unavailable and the collapse control renders its icon name as text. */
    button[data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] > button {{
        font-size: 0 !important;
    }}
    button[data-testid="stSidebarCollapseButton"]::after,
    [data-testid="stSidebarCollapseButton"] > button::after {{
        content: "‹";
        font-family: Arial, sans-serif;
        font-size: 1.55rem;
        line-height: 1;
        color: {TXT} !important;
    }}
    button[data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapsedControl"] > button {{
        font-size: 0 !important;
    }}
    button[data-testid="stSidebarCollapsedControl"]::after,
    [data-testid="stSidebarCollapsedControl"] > button::after {{
        content: "›";
        font-family: Arial, sans-serif;
        font-size: 1.55rem;
        line-height: 1;
        color: {TXT} !important;
    }}

    /* ── Scrollbar ────────────────────────────────────────────── */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: {BG};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {BORDER};
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {TXT2};
    }}

    /* ── Streamlit widgets — forçar dark ──────────────────────── */
    .stSelectbox div[data-baseweb="select"] {{
        background-color: {BG2} !important;
    }}
    .stSlider [data-testid="stTickBar"] {{
        background-color: {BORDER} !important;
    }}
    .stNumberInput input {{
        background-color: {BG2} !important;
        color: {TXT} !important;
    }}
    [data-testid="stExpander"] {{
        background-color: {BG2} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 10px;
    }}
    </style>
    """


# ─────────────────────────────────────────────────────────────────────────────
# Helpers Plotly
# ─────────────────────────────────────────────────────────────────────────────
def plotly_dark(fig, height=400):
    """Aplica estilo dark consistente a uma figura Plotly."""
    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG2,
        font=dict(color=TXT, family="IBM Plex Sans", size=12),
        height=height,
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=BORDER,
            borderwidth=1,
            font=dict(size=11),
        ),
    )
    fig.update_xaxes(
        gridcolor=BORDER, zerolinecolor=BORDER,
        title_font=dict(size=12), tickfont=dict(size=10),
    )
    fig.update_yaxes(
        gridcolor=BORDER, zerolinecolor=BORDER,
        title_font=dict(size=12), tickfont=dict(size=10),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# HTML helpers
# ─────────────────────────────────────────────────────────────────────────────
def badge(texto):
    """Pill decorativo (ex: 'Etapa 3 · Motor de Inferência')."""
    return f"<div class='badge'>{texto}</div>"


def theory(html):
    """Bloco de teoria/conceito (borda azul)."""
    return f"<div class='theory-box'>📘 {html}</div>"


def success(html):
    """Bloco de conclusão/resultado positivo (borda verde)."""
    return f"<div class='success-box'>✅ {html}</div>"


def warning(html):
    """Bloco de alerta/observação (borda amarela)."""
    return f"<div class='warning-box'>⚠️ {html}</div>"


def metric_card(titulo, valor, subtitulo=""):
    """Card de métrica compacto."""
    sub_html = f"<div class='mc-sub'>{subtitulo}</div>" if subtitulo else ""
    return (
        f"<div class='metric-card'>"
        f"  <div class='mc-title'>{titulo}</div>"
        f"  <div class='mc-value'>{valor}</div>"
        f"  {sub_html}"
        f"</div>"
    )


def cat_pill(categoria):
    """Pill inline colorido para um nome de categoria fuzzy."""
    cor = COR_CAT.get(categoria, TXT2)
    return (
        f"<span class='cat-pill' "
        f"style='background:rgba({_hex_to_rgb(cor)},0.18); color:{cor}; "
        f"border:1px solid {cor};'>"
        f"{categoria}</span>"
    )


def formula(html):
    """Bloco de fórmula centralizado."""
    return f"<div class='formula-box'>{html}</div>"


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades internas
# ─────────────────────────────────────────────────────────────────────────────
def _hex_to_rgb(hex_color):
    """Converte '#rrggbb' em 'r,g,b' para uso em rgba()."""
    h = hex_color.lstrip("#")
    return ",".join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))
