# Análise Fuzzy de Risco de Crédito Estruturado (CDOs)

**TE264 — Métodos Quantitativos Aplicados ao Risco · ITA Mestrado**

Aplicativo Streamlit que replica, de forma didática, a abordagem do artigo
*"Integração de Lógica Fuzzy e Modelagem de Dependência em Risco de Crédito
Estruturado: Abordagem Mamdani para PD e LGD"*, aplicada à análise dos modelos
de risco de CDOs e ao colapso de 2008.

## Tese central

A perda de crédito depende de dois parâmetros incertos — **PD** (probabilidade de
default) e **LGD** (perda dado o default). Em vez de tratá-los como números exatos,
o app os modela como **variáveis linguísticas fuzzy** e os combina por um **Sistema
de Inferência Mamdani** que produz um **Índice de Risco Composto (IRC)**. As
**cópulas** entram como camada complementar, modelando a dependência entre defaults —
o elo que os modelos pré-2008 subestimaram.

A lógica fuzzy trata a **incerteza epistêmica** (imprecisão sobre os parâmetros); as
cópulas e o Monte Carlo tratam a **incerteza aleatória** (variabilidade dos eventos).
São abordagens complementares.

## Estrutura

```
cdo_fuzzy_app/
├── app.py                       # navegação principal
├── application_walkthrough.py   # walkthrough em inglês para a candidatura
├── fuzzy_core.py                # motor Mamdani (núcleo testado)
├── theme.py                     # estilo dark IBM Plex + helpers
├── te264_historical_data.py     # dados calibrados (Moody's, Fed, Yale, FDIC, BIS)
├── requirements.txt
├── overview.py                  # Visão geral & tese
├── fuzzy_variables.py           # 1 · funções de pertinência triangulares
├── rule_bases.py                # 2 · três bases de regras + convergência
├── mamdani.py                   # 3 · inferência passo a passo + superfície 3D
├── copulas.py                   # 4 · dependência Gaussiana vs t-Student
├── monte_carlo.py               # 5 · Monte Carlo de 2ª ordem
├── possibility.py               # 6 · teoria da possibilidade + p-boxes
├── integration.py               # 7 · IRC fuzzy + cópula no portfólio CDO
└── tests/test_fuzzy_core.py     # testes do motor e da geração do portfólio
```

## Conceitos cobertos (objetivos de aprendizagem da disciplina)

- **Incerteza epistêmica vs. aleatória** — distinção formal e propagação conjunta
- **Conjuntos fuzzy** — funções de pertinência triangulares, fuzzificação
- **Sistema Mamdani** — fuzzificação → ativação (mín) → agregação (máx) → defuzzificação (centroide)
- **Cópulas** — Gaussiana vs. t-Student, dependência de cauda λ
- **Monte Carlo de 2ª ordem** — distribuição de distribuições, decomposição da incerteza
- **Teoria da Possibilidade** — medidas Π/N, p-boxes, transformação de Dubois-Prade

## Correspondência R → Python

| Funcionalidade        | R (disciplina)            | Python (app)             |
|-----------------------|---------------------------|--------------------------|
| Pertinência / números | sets, FuzzyNumbers        | scikit-fuzzy (trimf)     |
| Inferência Mamdani    | FRBS                      | scikit-fuzzy + numpy     |
| Defuzzificação        | FRBS, lfl                 | skfuzzy.defuzz           |
| Cópulas               | copula                    | scipy.stats + Cholesky   |
| Possibilidade / p-box | HYRISK                    | numpy (manual)           |
| Monte Carlo           | smc_basics.R              | numpy.random             |

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Application walkthrough (English)

The first page of the app is an English model walkthrough prepared for a Senior
Quantitative Analyst application. It documents data provenance, preparation, the
unit of observation, model selection, alternatives, validation, limitations,
production status, and how the prototype would be redesigned around a real
loan-month tape.

The portfolio included in this repository is **synthetic and calibrated to public
historical references**. It is not an observed lender loan tape, and the walkthrough
makes that limitation explicit.

## Testes

```bash
python -m unittest discover -s tests -v
```

## Fontes de calibração

Moody's "Corporate Default and Recovery Rates 1920–2010"; Fed Chicago "Default Rates
on Prime and Subprime Mortgages" (2010); Yale Journal of Financial Crises (2011);
FDIC WP 2015-06; BIS WP 1101; S&P Annual Default Study.
