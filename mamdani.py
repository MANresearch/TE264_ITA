# -*- coding: utf-8 -*-
"""Página 3: Sistema de inferência Mamdani - passo a passo e superfície de decisão."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import fuzzy_core as fc
import theme


def render():
    st.markdown(theme.badge("Etapa 3 · Motor de Inferência"), unsafe_allow_html=True)
    st.title("Sistema de Inferência Mamdani: PD x LGD -> IRC")
    st.markdown(
        theme.theory(
            "O sistema Mamdani combina as entradas fuzzificadas com a base de regras em "
            "<b>quatro etapas</b>: (1) fuzzificação das entradas; (2) avaliação das regras "
            "via operador AND = mínimo; (3) agregação dos consequentes pelo máximo; "
            "(4) defuzzificação por centroide. O resultado é o <b>Índice de Risco "
            "Composto (IRC)</b> - um valor em [0,1] interpretável de volta nas categorias "
            "linguísticas."
        ),
        unsafe_allow_html=True,
    )

    base = st.selectbox("Base de regras", list(fc.BASES_REGRAS.keys()), index=2)
    col1, col2 = st.columns(2)
    with col1:
        pd_val = st.slider("PD - Probabilidade de Default", 0.0, 1.0, 0.55, 0.01)
    with col2:
        lgd_val = st.slider("LGD - Perda Dado o Default", 0.0, 1.0, 0.60, 0.01)

    irc, det = fc.inferir_mamdani(pd_val, lgd_val, base=base, detalhar=True)
    cat_irc = det["categoria_irc"]
    cols = st.columns(4)
    cols[0].markdown(theme.metric_card("IRC", f"{irc:.3f}", "índice composto"), unsafe_allow_html=True)
    cols[1].markdown(theme.metric_card("Categoria", cat_irc, "classificação fuzzy"), unsafe_allow_html=True)
    cols[2].markdown(
        theme.metric_card("Regras ativas", str(len(det["regras_disparadas"])), "disparadas"),
        unsafe_allow_html=True,
    )
    el_proxy = pd_val * lgd_val
    cols[3].markdown(theme.metric_card("PD x LGD", f"{el_proxy:.3f}", "perda esperada (proxy)"), unsafe_allow_html=True)

    st.markdown("### Etapa 1 - Fuzzificação das entradas")
    c1, c2 = st.columns(2)
    for col, (nome, mu_dict, val) in zip(
        [c1, c2], [("PD", det["mu_pd"], pd_val), ("LGD", det["mu_lgd"], lgd_val)]
    ):
        with col:
            st.markdown(f"**{nome} = {val:.2f}**")
            for cat in fc.CATEGORIAS:
                if mu_dict[cat] > 0.001:
                    cor = theme.COR_CAT[cat]
                    st.markdown(
                        f"<div class='rule-fire'>{theme.cat_pill(cat)} "
                        f"<span style='color:{cor}'>μ = {mu_dict[cat]:.3f}</span></div>",
                        unsafe_allow_html=True,
                    )

    st.markdown("### Etapa 2 - Avaliação das regras (w = mín(μ_PD, μ_LGD))")
    if det["regras_disparadas"]:
        reg_df = pd.DataFrame(det["regras_disparadas"]).sort_values("w", ascending=False)
        for _, rr in reg_df.iterrows():
            cor = theme.COR_CAT[rr["irc"]]
            st.markdown(
                f"<div class='rule-fire'>SE PD={theme.cat_pill(rr['pd'])} "
                f"(μ={rr['mu_pd']:.2f}) E LGD={theme.cat_pill(rr['lgd'])} "
                f"(μ={rr['mu_lgd']:.2f}) ENTÃO IRC={theme.cat_pill(rr['irc'])} "
                f"<b style='color:{cor}'>-> w = {rr['w']:.3f}</b></div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("Nenhuma regra disparada para essa combinação.")

    st.markdown("### Etapas 3 e 4 - Agregação e defuzzificação por centroide")
    mfs = fc.funcoes_pertinencia()
    fig = go.Figure()
    for cat in fc.CATEGORIAS:
        cor = theme.COR_CAT[cat]
        fig.add_trace(
            go.Scatter(
                x=fc.UNIVERSO,
                y=mfs[cat],
                name=cat,
                mode="lines",
                line=dict(color=cor, width=1, dash="dot"),
                opacity=0.4,
            )
        )
    fig.add_trace(
        go.Scatter(
            x=fc.UNIVERSO,
            y=det["agregada"],
            name="Agregada",
            mode="lines",
            line=dict(color="#ffffff", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(79,195,247,0.25)",
        )
    )
    fig.add_vline(
        x=irc,
        line=dict(color=theme.VERM, width=3),
        annotation_text=f"IRC = {irc:.3f}",
        annotation_position="top",
    )
    fig.update_layout(
        title="Função de saída agregada e centroide (IRC)",
        xaxis_title="IRC [0, 1]",
        yaxis_title="Grau de pertinência μ",
        yaxis_range=[0, 1.05],
    )
    theme.plotly_dark(fig, height=380)
    st.plotly_chart(fig, width="stretch")
    st.markdown(
        theme.formula(
            f"IRC = ∫ y·μ_agg(y) dy / ∫ μ_agg(y) dy = <b>{irc:.4f}</b> -> "
            f"categoria <b>{cat_irc}</b>"
        ),
        unsafe_allow_html=True,
    )

    st.markdown("### Superfície de decisão IRC(PD, LGD)")
    st.markdown(
        theme.theory(
            "A superfície mostra o IRC para todas as combinações de PD e LGD. Ela "
            "revela o comportamento global do sistema: regiões planas (consenso) e "
            "regiões de transição abrupta (onde pequenas mudanças nos parâmetros "
            "alteram a classificação de risco)."
        ),
        unsafe_allow_html=True,
    )
    with st.spinner("Calculando superfície..."):
        pdg, lgdg, z = fc.superficie_decisao(base=base, n=33)
    fig3d = go.Figure(
        data=[
            go.Surface(
                x=pdg,
                y=lgdg,
                z=z.T,
                colorscale=[
                    [0, theme.VERDE],
                    [0.33, theme.AMARELO],
                    [0.66, theme.LARANJA],
                    [1, theme.VERM],
                ],
                cmin=0,
                cmax=1,
                colorbar=dict(title="IRC", tickfont=dict(color=theme.TXT)),
            )
        ]
    )
    fig3d.add_trace(
        go.Scatter3d(
            x=[pd_val],
            y=[lgd_val],
            z=[irc],
            mode="markers",
            marker=dict(color="#ffffff", size=6, line=dict(color="#000", width=1)),
            name="Ponto atual",
        )
    )
    fig3d.update_layout(
        title="Superfície de Decisão do Sistema Fuzzy",
        scene=dict(
            xaxis_title="PD",
            yaxis_title="LGD",
            zaxis_title="IRC",
            xaxis=dict(backgroundcolor=theme.BG2, gridcolor=theme.BORDER, color=theme.TXT),
            yaxis=dict(backgroundcolor=theme.BG2, gridcolor=theme.BORDER, color=theme.TXT),
            zaxis=dict(backgroundcolor=theme.BG2, gridcolor=theme.BORDER, color=theme.TXT),
        ),
        paper_bgcolor=theme.BG,
        font=dict(color=theme.TXT, family="IBM Plex Sans"),
        height=560,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig3d, width="stretch")
    st.markdown(
        theme.success(
            "A superfície é <b>globalmente crescente</b> com PD e LGD, com pequenas "
            "oscilações locais nas regiões de sobreposição das funções de pertinência. "
            "A sensibilidade é ligeiramente maior no eixo da PD - a predominância da PD "
            "que o próximo gráfico quantifica e que o artigo destaca como achado central "
            "(Seção 4.4.1)."
        ),
        unsafe_allow_html=True,
    )
    st.caption(
        "Implementação: fuzzy_core.inferir_mamdani (min-max + centroide via "
        "skfuzzy.defuzz). Correspondência com FRBS (R) - frbs.learn / predict."
    )
