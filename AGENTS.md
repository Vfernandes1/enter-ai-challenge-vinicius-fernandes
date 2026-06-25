Agent patterns and conventions for this repository

Purpose
- Provide a concise pattern for other agents or automation to interact with this project (run/report/simulate).

Conventions
- Entrypoint: `python3 main.py` runs the canonical report generation flow and emits Markdown, PDF, JSON summary and CSV breakdown.
- Simulation: `PYTHONPATH=. python3 rivet_workflow/simulated_rivet_workflow.py` runs the deterministic Rivet-style simulation that logs node outputs and writes `rivet_workflow_spec.json` and `rivet_workflow_spec.yaml`.

Agent responsibilities
- Data ingestion: read `app/inputs/client_data.json` and `app/inputs/macro_data.json`.
- Deterministic computation: call `PortfolioEngine` methods in order: `calculate_monthly_profitability()`, `evaluate_macro_impact()`, `generate_recommendations()`, `assess_risk_alignment()` and `build_letter()`.
- Exports: ensure downstream artifacts exist: `monthly_report_albert.md`, `monthly_report_albert.pdf`, `monthly_report_summary.json`, `monthly_report_albert.csv`.

How to implement a new automated agent
1. Create a small runner script (e.g. `agents/your_agent.py`).
2. Respect the order of operations above; methods are idempotent and safe to re-run.
3. Write logs and artifacts into `agents/` or `rivet_workflow/` for traceability.
4. Include prompt templates and node metadata in any simulation spec so human reviewers can reproduce steps.

Testing and CI
- Agents should run `python3 main.py` in a clean environment and validate that the four artifacts exist.
- For reproducibility include `PYTHONPATH=.` when running simulation code that imports `app` from the repo root.

Notes
- This repository is deterministic by design; where randomization would be used, prefer seeded inputs or store seeds in the artifact metadata.
- If an agent needs to call an external LLM, it should record the prompt, model, and response in `rivet_workflow/` for auditability.

Example quick-run (local):

```bash
pip install reportlab
python3 main.py
PYTHONPATH=. python3 rivet_workflow/simulated_rivet_workflow.py
```
