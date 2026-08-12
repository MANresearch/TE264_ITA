# -*- coding: utf-8 -*-
"""Página 7: Integração - IRC fuzzy + cópula aplicados a um portfólio CDO."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

import fuzzy_core as fc
import theme
from te264_historical_data import gerar_portfolio_calibrado


@st.cache_data
def _portfolio(n, cenario, seed):
    return gerar_portfolio_calibrado(n=n, cenario=cenario, seed=seed)


def _irc_portfolio(df):
    """Calcula o IRC fuzzy de cada ativo e o IRC ponderado do portfólio."""
    ircs = np.array(
        [fc.inferir_mamdani(row.pd, row.lgd, base="Especialista") for row in df.itertuples()]
    )
    ead = df["ead"].values
    irc_ptf = np.sum(ircs * ead) / np.sum(ead)
    return ircs, irc_ptf


def render():
    st.markdown(theme.badge("Etapa 7 · Síntese"), unsafe_allow_html=True)
    st.title("Integração: IRC Fuzzy + Cópula no Portfólio CDO")
    st.markdown(
        theme.theory(
            "Esta página reúne todas as camadas: um portfólio CDO calibrado a dados "
            "históricos, o <b>IRC fuzzy</b> calculado para cada ativo pelo motor Mamdani, "
            "e a <b>simulação com cópula</b> que captura a dependência entre defaults. O "
            "resultado é uma visão completa do risco - pontual e de cauda, aleatório e "
            "epistêmico."
        ),
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        n = st.select_slider("Número de ativos", [200, 500, 1000], value=500)
    with c2:
        cenario = st.selectbox(
            "Cenário",
            ["normal", "stress", "crise_2008"],
            format_func=lambda x: {
                "normal": "Normal",
                "stress": "Estresse",
                "crise_2008": "Crise 2008",
            }[x],
        )
    with c3:
        seed = st.number_input("Semente", 1, 999, 42)

    df = _portfolio(n, cenario, seed)
    ircs, irc_ptf = _irc_portfolio(df)
    df = df.assign(irc=ircs, irc_cat=[fc.irc_para_categoria(v) for v in ircs])
    ead_total = df["ead"].sum()
    el_total = df["el"].sum()
    cols = st.columns(4)
    cols[0].markdown(
        theme.metric_card("EAD total", f"R$ {ead_total / 1_000_000:.1f}M", f"{n} ativos"),
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        theme.metric_card(
            "Perda esperada",
            f"R$ {el_total / 1_000_000:.2f}M",
            f"{100 * el_total / ead_total:.2f}% do EAD",
        ),
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        theme.metric_card("IRC do portfólio", f"{irc_ptf:.3f}", fc.irc_para_categoria(irc_ptf)),
        unsafe_allow_html=True,
    )
    cols[3].markdown(
        theme.metric_card(
            "PD / LGD médios",
            f"{df['pd'].mean():.1%} / {df['lgd'].mean():.0%}",
            "ponderado simples",
        ),
        unsafe_allow_html=True,
    )

    st.markdown("### Distribuição do IRC fuzzy por ativo")
    c1, c2 = st.columns([3, 2])
    with c1:
        fig = go.Figure()
        for cat in fc.CATEGORIAS:
            sub = df[df["irc_cat"] == cat]
            if len(sub):
                fig.add_trace(
                    go.Histogram(
                        x=sub["irc"],
                        name=cat,
                        marker_color=theme.COR_CAT[cat],
                        opacity=0.85,
                        xbins=dict(size=0.05),
                    )
                )
        fig.add_vline(
            x=irc_ptf,
            line=dict(color="#fff", width=2.5, dash="dash"),
            annotation_text=f"IRC portfólio = {irc_ptf:.3f}",
        )
        fig.update_layout(
            barmode="stack",
            title="Histograma de IRC dos ativos",
            xaxis_title="IRC",
            yaxis_title="Nº de ativos",
        )
        theme.plotly_dark(fig, height=400)
        st.plotly_chart(fig, width="stretch")
    with c2:
        dist_cat = df["irc_cat"].value_counts().reindex(fc.CATEGORIAS).fillna(0)
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=fc.CATEGORIAS,
                    values=dist_cat.values,
                    marker=dict(colors=[theme.COR_CAT[c] for c in fc.CATEGORIAS]),
                    hole=0.45,
                    textinfo="label+percent",
                )
            ]
        )
        fig.update_layout(
            title="Composição por categoria de risco",
            paper_bgcolor=theme.BG,
            font=dict(color=theme.TXT),
            height=400,
            showlegend=False,
        )
        st.plotly_chart(fig, width="stretch")

    st.markdown("### IRC por setor")
    setor_irc = (
        df.groupby("setor")
        .agg(irc_medio=("irc", "mean"), ead=("ead", "sum"), n=("id", "count"))
        .reset_index()
        .sort_values("irc_medio", ascending=True)
    )
    fig = go.Figure()
    cores_setor = [theme.COR_CAT[fc.irc_para_categoria(v)] for v in setor_irc["irc_medio"]]
    fig.add_trace(
        go.Bar(
            y=setor_irc["setor"],
            x=setor_irc["irc_medio"],
            orientation="h",
            marker_color=cores_setor,
            text=[f"{v:.3f}" for v in setor_irc["irc_medio"]],
            textposition="auto",
        )
    )
    fig.update_layout(title="IRC médio por setor", xaxis_title="IRC", yaxis_title="")
    theme.plotly_dark(fig, height=320)
    st.plotly_chart(fig, width="stretch")

    st.markdown("### Perda do portfólio com dependência (cópula t)")
    st.markdown(
        theme.theory(
            "Agora simulamos as perdas considerando que os defaults são <b>dependentes</b> "
            "via cópula t-Student. Comparamos com o caso independente para ver quanto a "
            "correlação engorda a cauda - o efeito que destruiu as tranches Senior em 2008."
        ),
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        rho = st.slider("Correlação ρ", 0.0, 0.9, 0.45, 0.05)
    with c2:
        df_cop = st.slider("ν (cópula t)", 2, 20, 4, 1)

    n_sim = 2000
    with st.spinner("Simulando perdas com cópula..."):
        rng = np.random.default_rng(int(seed))
        pd_arr = df["pd"].values
        lgd_arr = df["lgd"].values
        ead_arr = df["ead"].values
        m = len(df)

        def simular(usar_dependencia):
            perdas = np.zeros(n_sim)
            for s in range(n_sim):
                if usar_dependencia:
                    g = rng.chisquare(df_cop) / df_cop
                    fator = rng.standard_normal()
                    eps = rng.standard_normal(m)
                    lat = (np.sqrt(rho) * fator + np.sqrt(1 - rho) * eps) / np.sqrt(g)
                    u = stats.t.cdf(lat, df_cop)
                else:
                    u = rng.random(m)
                default = u < pd_arr
                perdas[s] = np.sum(default * lgd_arr * ead_arr)
            return perdas

        perdas_dep = simular(True)
        perdas_ind = simular(False)

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=perdas_ind / 1_000_000,
            name="Independente",
            marker_color=theme.AZUL,
            opacity=0.6,
            nbinsx=50,
        )
    )
    fig.add_trace(
        go.Histogram(
            x=perdas_dep / 1_000_000,
            name="Cópula t (dependente)",
            marker_color=theme.VERM,
            opacity=0.6,
            nbinsx=50,
        )
    )
    var99_dep = np.percentile(perdas_dep, 99) / 1_000_000
    var99_ind = np.percentile(perdas_ind, 99) / 1_000_000
    fig.add_vline(
        x=var99_dep,
        line=dict(color=theme.VERM, width=2, dash="dash"),
        annotation_text=f"VaR99 dep = {var99_dep:.1f}M",
    )
    fig.add_vline(
        x=var99_ind,
        line=dict(color=theme.AZUL, width=2, dash="dot"),
        annotation_text=f"VaR99 ind = {var99_ind:.1f}M",
    )
    fig.update_layout(
        barmode="overlay",
        title="Distribuição de perdas: dependente vs. independente",
        xaxis_title="Perda (R$ milhões)",
        yaxis_title="Frequência",
    )
    theme.plotly_dark(fig, height=420)
    st.plotly_chart(fig, width="stretch")

    es99_dep = perdas_dep[perdas_dep >= np.percentile(perdas_dep, 99)].mean() / 1_000_000
    cols = st.columns(4)
    cols[0].markdown(
        theme.metric_card("VaR 99% (dependente)", f"R$ {var99_dep:.1f}M", "com cópula t"),
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        theme.metric_card("VaR 99% (independente)", f"R$ {var99_ind:.1f}M", "sem dependência"),
        unsafe_allow_html=True,
    )
    amp = var99_dep / var99_ind if var99_ind > 0 else 0
    cols[2].markdown(
        theme.metric_card("Amplificação de cauda", f"{amp:.2f}x", "efeito da correlação"),
        unsafe_allow_html=True,
    )
    cols[3].markdown(
        theme.metric_card("Expected Shortfall 99%", f"R$ {es99_dep:.1f}M", "perda média na cauda"),
        unsafe_allow_html=True,
    )
    st.markdown(
        theme.warning(
            f"A dependência via cópula amplia o VaR 99% em <b>{amp:.2f}x</b> em relação "
            "ao caso independente. Esse é o mecanismo central da crise de 2008: os "
            "modelos assumiam baixa correlação (ou cópula Gaussiana sem tail dependence), "
            "e a realidade dos defaults sincronizados produziu perdas muito além do VaR "
            "reportado - destruindo tranches que pareciam seguras."
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        theme.success(
            "<b>Síntese do projeto:</b> a lógica fuzzy nos deu um IRC interpretável e "
            "auditável para cada ativo, tornando explícita a imprecisão dos parâmetros "
            "(incerteza epistêmica). As cópulas modelaram a dependência entre defaults "
            "(estrutura da incerteza aleatória). O Monte Carlo de 2ª ordem e a Teoria da "
            "Possibilidade quantificaram a largura da nossa ignorância. Juntas, essas "
            "ferramentas mostram o que um único número de VaR esconde - e que ignorar "
            "essa incerteza tem consequências sistêmicas."
        ),
        unsafe_allow_html=True,
    )
    with st.expander("Ver amostra do portfólio"):
        st.dataframe(
            df[["id", "setor", "rating", "pd", "lgd", "ead", "irc", "irc_cat"]]
            .head(50)
            .round(4),
            width="stretch",
            hide_index=True,
        )
    st.caption(
        "Implementação: portfólio calibrado (te264_historical_data) + IRC fuzzy "
        "(fuzzy_core) + simulação de fator único com cópula t (scipy.stats). Integra "
        "todas as camadas: fuzzy, cópula, Monte Carlo e dados históricos reais."
    )
