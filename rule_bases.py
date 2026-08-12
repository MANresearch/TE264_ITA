# -*- coding: utf-8 -*-
"""Página 2: As três bases de regras elicitadas e análise de convergência."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import fuzzy_core as fc
import theme


def _heatmap_regras(base, titulo):
    """Heatmap 4x4 de uma base de regras (índice de categoria como cor)."""
    z = fc.matriz_categoria_para_indice(base)
    texto = fc.BASES_REGRAS[base]
    colorscale = [
        [0.0, theme.VERDE],
        [0.33, theme.AMARELO],
        [0.66, theme.LARANJA],
        [1.0, theme.VERM],
    ]
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=fc.CATEGORIAS,
            y=fc.CATEGORIAS,
            text=texto,
            texttemplate="%{text}",
            textfont=dict(size=12, family="IBM Plex Mono"),
            colorscale=colorscale,
            showscale=False,
            zmin=0,
            zmax=3,
            xgap=3,
            ygap=3,
        )
    )
    fig.update_layout(
        title=titulo,
        xaxis_title="LGD ->",
        yaxis_title="PD ->",
        yaxis=dict(autorange="reversed"),
    )
    theme.plotly_dark(fig, height=340)
    return fig


def render():
    st.markdown(theme.badge("Etapa 2 · Base de Conhecimento"), unsafe_allow_html=True)
    st.title("Bases de Regras Fuzzy Elicitadas")
    st.markdown(
        theme.theory(
            "O coração de um sistema Mamdani é a <b>base de regras</b> - um conjunto "
            "de proposições do tipo <i>SE PD é Alto E LGD é Moderado, ENTÃO IRC é "
            "Crítico</i>. Com 4 categorias para PD e 4 para LGD, há <b>16 regras</b> "
            "(uma matriz 4x4). O artigo elicitou essa matriz de <b>três fontes "
            "independentes</b>: ChatGPT, Claude e um Especialista humano (José "
            "Monteiro Varanda Neto, 20+ anos de experiência). A matriz do Especialista "
            "(Tabela 8) é a base final adotada."
        ),
        unsafe_allow_html=True,
    )
    st.markdown("### As três matrizes de regras")
    st.caption("Linhas = categoria de PD · Colunas = categoria de LGD · Célula = IRC resultante")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(_heatmap_regras("ChatGPT", "Fonte A · ChatGPT"), width="stretch")
    with c2:
        st.plotly_chart(_heatmap_regras("Claude", "Fonte B · Claude"), width="stretch")
    with c3:
        st.plotly_chart(_heatmap_regras("Especialista", "Fonte C · Especialista ★"), width="stretch")

    st.markdown(
        theme.success(
            "★ A matriz do <b>Especialista</b> é a base final do sistema. Note seu "
            "padrão mais conservador: a diagonal e o canto inferior-direito (PD e LGD "
            "altos) escalam rapidamente para Crítico, refletindo a aversão a risco de "
            "um gestor experiente."
        ),
        unsafe_allow_html=True,
    )
    st.markdown("### Convergência entre as fontes")
    conv = fc.analise_convergencia()
    cols = st.columns(4)
    cols[0].markdown(
        theme.metric_card("Concordância total", f"{conv['concordancia_total']}/16", "as 3 fontes idênticas"),
        unsafe_allow_html=True,
    )
    cols[1].markdown(
        theme.metric_card("Concordância parcial", f"{conv['concordancia_parcial']}/16", "2 de 3 concordam"),
        unsafe_allow_html=True,
    )
    cols[2].markdown(
        theme.metric_card("Divergência total", f"{conv['divergencia_total']}/16", "3 respostas distintas"),
        unsafe_allow_html=True,
    )
    taxa = 100 * conv["concordancia_total"] / conv["total_combinacoes"]
    cols[3].markdown(
        theme.metric_card("Taxa de consenso", f"{taxa:.0f}%", "convergência total"),
        unsafe_allow_html=True,
    )

    st.markdown("#### Mapa de convergência célula a célula")
    mapa = conv["mapa"]
    cod = {"total": 2, "parcial": 1, "divergente": 0}
    zc = np.array([[cod[mapa[i][j]] for j in range(4)] for i in range(4)])
    txt = [
        [
            "✓✓✓" if mapa[i][j] == "total" else "✓✓·" if mapa[i][j] == "parcial" else "✗✗✗"
            for j in range(4)
        ]
        for i in range(4)
    ]
    fig = go.Figure(
        data=go.Heatmap(
            z=zc,
            x=fc.CATEGORIAS,
            y=fc.CATEGORIAS,
            text=txt,
            texttemplate="%{text}",
            textfont=dict(size=13, family="IBM Plex Mono"),
            colorscale=[[0, theme.VERM], [0.5, theme.AMARELO], [1, theme.VERDE]],
            showscale=False,
            zmin=0,
            zmax=2,
            xgap=3,
            ygap=3,
        )
    )
    fig.update_layout(
        title="Verde = consenso total · Amarelo = parcial · Vermelho = divergência",
        xaxis_title="LGD ->",
        yaxis_title="PD ->",
        yaxis=dict(autorange="reversed"),
    )
    theme.plotly_dark(fig, height=340)
    st.plotly_chart(fig, width="stretch")

    if conv["celulas_divergentes"]:
        st.markdown("#### Onde as fontes discordam")
        df = pd.DataFrame(conv["celulas_divergentes"]).rename(columns={"pd": "PD", "lgd": "LGD"})
        st.dataframe(df, width="stretch", hide_index=True)

    st.markdown(
        theme.warning(
            f"Calculando célula a célula, encontramos <b>{conv['concordancia_total']} de "
            f"consenso total e {conv['concordancia_parcial']} parcial</b>, sem nenhuma "
            "divergência completa (as três fontes nunca dão três respostas totalmente "
            "distintas). <b>Observação para o manuscrito:</b> o texto do artigo (Tabela 6) "
            "relata 11 totais + 5 parciais; a contagem direta das matrizes publicadas dá "
            "12 + 4. Vale reconciliar essa diferença na versão final."
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        theme.theory(
            "A alta convergência (75% de consenso total) sugere que a estrutura de risco "
            "PD x LGD -> IRC é <b>robusta</b>: fontes independentes chegam a conclusões "
            "semelhantes. As divergências concentram-se nas <b>bordas</b> (combinações "
            "extremas de PD ou LGD), onde o julgamento subjetivo pesa mais - precisamente "
            "onde a elicitação de especialistas agrega mais valor."
        ),
        unsafe_allow_html=True,
    )
    st.caption(
        "Matrizes transcritas das Tabelas 3, 4 e 8 do artigo. Implementação: "
        "fuzzy_core.BASES_REGRAS + analise_convergencia()."
    )
