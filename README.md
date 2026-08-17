# Dermalyze Expert System

A rule-based expert system prototype for early risk screening of skin lesions, combining **Forward Chaining** inference with **Certainty Factor** reasoning.

## Important disclaimer

**Dermalyze is a student project, not a medical device.**

It does not diagnose skin cancer or any other condition. It is a prototype built to explore how classical expert systems handle uncertainty, and its knowledge base is small and academic. A result from this tool carries no clinical meaning.

If you are concerned about a mole or a skin lesion, please see a dermatologist. Do not use this, or any web tool, to decide whether something is safe to ignore.

## Background

The project studies a classic AI problem: how to reason toward a conclusion when none of the inputs are certain. Skin lesion screening fits that well, because symptoms are reported by someone who is unsure, and rules point toward a condition without ever proving it.

Rather than reaching for a neural network, the aim was to implement the older symbolic approach by hand and see how far it gets.

## How it works

1. **Symptom questionnaire.** The user answers a set of clinical questions and states how confident they are about each answer.
2. **Forward chaining.** The inference engine starts from the reported symptoms and repeatedly fires matching rules until no new facts can be derived.
3. **Certainty Factor.** Each rule carries a confidence weight. CF values are combined as evidence accumulates, so two weak signals pointing the same way strengthen the conclusion without either being treated as proof.
4. **Explanation facility.** Backward chaining reconstructs the chain of rules behind a result, so the system can answer "why did you conclude that?" rather than only printing a verdict.
5. **Report and history.** Results are written into a readable report, and past consultations are retained so answers can be compared.

## Project structure

```
├── app.py                  # Streamlit UI and application flow
├── knowledge_base.py       # Loads and indexes the JSON knowledge base
├── inference_engine.py     # Forward chaining engine
├── backward_chaining.py    # Explanation facility
├── certainty_factor.py     # CF combination math
├── report_generator.py     # Builds the consultation report
├── validators.py           # Input validation
└── data/
    ├── gejala.json         # Symptoms
    ├── penyakit.json       # Conditions
    ├── rules.json          # Production rules with CF weights
    ├── edukasi.json        # Educational content
    └── test_cases.json     # Test cases for the engine
```

The knowledge base lives entirely in JSON, so rules and symptoms can be edited without touching the Python.

## Built with

- **Python**
- **Streamlit** for the interface
- **pandas** for data handling
- **Plotly** for visualising certainty scores

## Requirements

Python 3.9 or newer.

## Running it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will open the application in your browser, usually at `http://localhost:8501`.

## Note on language

The interface, the knowledge base, and the generated reports are written in Indonesian, since the system was built for an Indonesian audience.
