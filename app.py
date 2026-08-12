# -*- coding: utf-8 -*-
"""
TE264 — Métodos Quantitativos Aplicados ao Risco · ITA Mestrado
═══════════════════════════════════════════════════════════════════════════════
Análise Fuzzy de Risco de Crédito Estruturado (CDOs)
Abordagem Mamdani PD × LGD → IRC, com cópulas, Monte Carlo de 2ª ordem
e Teoria da Possibilidade como camadas complementares.

Refatorado para alinhar ao artigo:
"Integração de Lógica Fuzzy e Modelagem de Dependência em Risco de Crédito
 Estruturado: Abordagem Mamdani para PD e LGD"
"""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import theme
import application_walkthrough
import overview
import fuzzy_variables
import rule_bases
import mamdani
import copulas
import monte_carlo
import possibility
import integration

st.set_page_config(
    page_title="TE264 · Fuzzy CDO Risk",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(theme.inject_css(), unsafe_allow_html=True)

PAGINAS = {
    "Application Walkthrough (EN)": application_walkthrough,
    "Visão Geral & Tese":            overview,
    "1 · Variáveis Fuzzy":           fuzzy_variables,
    "2 · Bases de Regras":           rule_bases,
    "3 · Inferência Mamdani":        mamdani,
    "4 · Cópulas (Dependência)":     copulas,
    "5 · Monte Carlo 2ª Ordem":      monte_carlo,
    "6 · Teoria da Possibilidade":   possibility,
    "7 · Integração no Portfólio":   integration,
}

with st.sidebar:
    st.markdown("## ◆ TE264 · ITA")
    st.markdown("**Análise Fuzzy de Risco de CDOs**")
    st.caption("Abordagem Mamdani · PD × LGD → IRC")
    st.markdown("---")

    escolha = st.radio("Navegação", list(PAGINAS.keys()), label_visibility="collapsed")

    st.markdown("---")
    st.caption(
        "Métodos Quantitativos Aplicados ao Risco\n\n"
        "Incerteza epistêmica/aleatória · Conjuntos fuzzy · "
        "Cópulas · Monte Carlo 2ª ordem · Teoria da possibilidade"
    )
    st.caption("Correspondência R → Python:\n`sets/FuzzyNumbers/FRBS/lfl` → `scikit-fuzzy`")

# Renderiza a página selecionada
PAGINAS[escolha].render()
