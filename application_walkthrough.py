# -*- coding: utf-8 -*-
"""English walkthrough prepared for the SixPoint Senior Quantitative Analyst application."""

import streamlit as st

import theme


def render():
    st.markdown(theme.badge("SixPoint Application · Model Walkthrough"), unsafe_allow_html=True)
    st.title("From Epistemic Uncertainty to Portfolio Tail Risk")
    st.caption(
        "Matheus de Azevedo Nascimento · TE-264, Instituto Tecnológico de Aeronáutica (ITA) · 2026"
    )
    st.markdown(
        theme.theory(
            "<b>What I built with my co-authors:</b> an interpretable credit-risk "
            "laboratory that combines a Mamdani fuzzy inference system for PD/LGD "
            "imprecision with t-copula dependence and Monte Carlo loss simulation. "
            "The model is a research prototype, not a production underwriting or "
            "loan-surveillance system. This walkthrough makes that boundary explicit."
        ),
        unsafe_allow_html=True,
    )

    st.markdown("### 1. The decision problem")
    st.write(
        "Traditional portfolio models often treat probability of default (PD) and loss "
        "given default (LGD) as precise point estimates. In thin-data settings, however, "
        "those inputs also embed expert judgment and estimation uncertainty. At the same "
        "time, portfolio losses depend on whether defaults cluster in the tail. The model "
        "therefore separates two questions: how imprecise are the marginal risk inputs, "
        "and how dependent are the default events?"
    )

    st.markdown("### 2. Data provenance and preparation")
    st.write(
        "The public repository does not contain a raw lender loan tape. It creates a "
        "synthetic portfolio calibrated to published historical studies from Moody's, "
        "the Federal Reserve, Yale Journal of Financial Crises, the FDIC, BIS and S&P. "
        "Sector/scenario assumptions specify PD, LGD and EAD distributions for normal, "
        "stress and 2008-crisis conditions."
    )
    st.markdown(
        "Preparation is deterministic and auditable: sector weights are normalized; "
        "a seeded generator allocates assets; PD and LGD draws are clipped to valid "
        "ranges; EAD is floored above zero; simplified ratings are mapped from PD; and "
        "expected loss is calculated as `PD × LGD × EAD`."
    )
    st.markdown(
        theme.warning(
            "<b>Important limitation:</b> these are calibrated assumptions, not cleaned "
            "observations from an originator's servicing history. They support method "
            "demonstration and stress comparison, but not empirical claims about a live "
            "pool."
        ),
        unsafe_allow_html=True,
    )

    st.markdown("### 3. Unit of observation - and what I would change for a lender tape")
    st.write(
        "The current unit is one static asset record: asset ID, sector, rating, PD, LGD, "
        "EAD and expected loss. That is adequate for illustrating cross-sectional fuzzy "
        "classification and portfolio loss dependence, but it cannot model delinquency "
        "migration, cure, prepayment, seasoning or path dependency."
    )
    st.write(
        "For SixPoint's use case, I would rebuild the analytical base as a loan-month "
        "panel, keyed by loan ID and reporting month. It would retain contractual terms, "
        "origination cohort, opening/closing balance, cash collections, DPD state, "
        "modifications, recoveries and terminal events. That construction is necessary "
        "for roll-rate matrices, vintage curves, discrete-time hazard models and "
        "competing risks for default versus prepayment; it also makes censoring, "
        "survivorship bias and cure behavior visible rather than collapsing them away."
    )

    st.markdown("### 4. Model choice and alternatives considered")
    choices = {
        "Mamdani fuzzy system": (
            "Chosen because expert classifications such as low/moderate/high/critical "
            "are gradual and because every fired rule remains inspectable. Sixteen PD-LGD "
            "rules combine by min-max inference and centroid defuzzification into a "
            "composite risk index (IRC)."
        ),
        "t-copula": (
            "Chosen alongside the Gaussian copula to expose tail dependence and the "
            "impact of clustered defaults on VaR and Expected Shortfall."
        ),
        "Second-order Monte Carlo": (
            "Separates parameter uncertainty in PD/LGD from randomness in default events "
            "instead of mixing both sources into one confidence interval."
        ),
        "Alternatives": (
            "A binary classifier would be insufficient for timing, censoring and "
            "prepayment. With a real monthly tape, I would benchmark a transparent "
            "roll-rate/Markov model and a discrete hazard competing-risks model before "
            "considering more complex machine-learning specifications."
        ),
    }
    for label, text in choices.items():
        st.markdown(f"**{label}.** {text}")

    st.markdown("### 5. Testing, evaluation and findings")
    st.write(
        "This is not a supervised-learning model, so there is no train/test split or "
        "out-of-sample AUC to report. Validation focused on structure, reproducibility "
        "and sensitivity:"
    )
    st.markdown(
        "- Cross-source rule review: the ChatGPT, Claude and human-expert rule matrices "
        "agree fully in 12 of 16 cells and partially in the remaining four."
    )
    st.markdown(
        "- Boundary checks: the expert system returns an IRC near 0.113 at the lowest "
        "PD/LGD corner and 0.890 at the highest corner, with no missing values."
    )
    st.markdown(
        "- Surface diagnostics: risk broadly rises with PD and LGD, but centroid "
        "defuzzification creates small local oscillations (less than 0.01 on a 41×41 "
        "grid). I would not describe the surface as strictly monotonic without adding "
        "constraints or redesigning overlapping membership functions."
    )
    st.markdown(
        "- Scenario and dependence tests: fixed seeds make results reproducible; normal, "
        "stress and crisis calibrations separate parameter effects; dependent and "
        "independent loss simulations isolate tail amplification."
    )

    st.markdown("### 6. Production status and monitoring")
    st.write(
        "The deliverable is deployed as an interactive Streamlit research application. "
        "The calculation engine is separated from the presentation layer and can be "
        "tested directly. It has not been used to approve loans, price a facility or set "
        "a covenant. A production path would add versioned raw-data snapshots, schema and "
        "reconciliation checks, test coverage, model governance, access controls and "
        "scheduled monitoring of data quality, calibration, roll rates, vintage drift, "
        "covenant headroom and realized-versus-expected losses."
    )

    st.markdown("### 7. Decisions and trade-offs I would defend")
    st.markdown(
        "1. I chose interpretability over a black-box score because the central question "
        "was how to formalize expert uncertainty, not how to maximize a predictive metric."
    )
    st.markdown(
        "2. I kept epistemic and aleatory uncertainty separate so an investment committee "
        "can see whether risk comes from fragile inputs or clustered outcomes."
    )
    st.markdown(
        "3. I treat the synthetic calibration as a limitation, not as evidence. A real "
        "investment decision would start with loan-level reconciliation and panel design."
    )
    st.markdown(
        "4. I would use the fuzzy index as a transparent overlay or challenger, not a "
        "replacement for cash-flow, roll-rate, survival and covenant models."
    )

    st.markdown(
        theme.success(
            "<b>Relevance to SixPoint:</b> the project shows how I structure ambiguous "
            "risk inputs, make model assumptions inspectable and test the effect of "
            "dependence on portfolio tails. Just as important, it shows where I would "
            "change the analytical design when moving from a research prototype to a "
            "messy emerging-market loan tape."
        ),
        unsafe_allow_html=True,
    )
    st.caption(
        "Navigate through the modules in the sidebar to inspect membership functions, "
        "rule elicitation, Mamdani inference, copulas, Monte Carlo, possibility theory "
        "and the integrated portfolio simulation."
    )
