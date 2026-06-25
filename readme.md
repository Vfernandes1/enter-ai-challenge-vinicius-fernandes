# AI Financial Advisor for XP Customers
*(Enter working session)*

## Context
XP is an investment management company with a network of 20,000+ financial advisors that offer a personal touch to its clients and are responsible for managing key accounts by:
* **(i)** Explaining fluctuations in a client’s investment portfolio.
* **(ii)** Outlining current market trends to clients in lay terms.
* **(iii)** Recommending investment opportunities that are aligned with clients’ risk profiles.

Each financial advisor is responsible for a range of between 50 and 300 clients. XP is struggling to deliver high-quality, tailored advice to all its clients, especially **“middle market”** ones that have less than R$1 million managed through an XP account. 

XP has hired you to build a proof-of-concept language model workflow that will empower financial advisors to manage three times as many middle market clients as they currently do. The company’s goal is to grow its client NPS and share of wallet in this segment.

---

## Objective
Your team’s mission is to build an application that sends a monthly report to every XP client, explaining:
1. How their investment portfolio performed.
2. How market events may affect their portfolio in the future.
3. How they should consider adjusting their portfolio in a way that is compatible with **A)** their risk profile, and **B)** recommendations set forth by investment research professionals.

---

## Challenge
A first version of the MVP has been built by your team — but it does not meet the quality standards we want to present to XP leadership tomorrow. Your task is to review and iterate on the current product to bring it to a level you’d be proud to present.

**Your mission is to:**
1. Carefully review the current output and workflow.
2. Identify quality issues or inconsistencies.
3. Pick one of the improvement areas below (or combine them, if time allows).
4. Make the improvements and document your reasoning.

### Suggested Improvement Areas
*(Pick at least one of the areas below)*
* **Portfolio Profitability Calculation:** Calculate the portfolio’s return for last month and present the information going beyond a basic return calculation. For example, use external data sources or present the information with additional context and/or visual elements that help the client better understand his/her performance.
* **Buy/Sell Recommendation Logic:** Improve the recommendation logic by adding a module that recommends which assets the client should consider buying or selling.
* **Automated Formatting:** Improve the output generation logic to create a professional-looking letter, ready to be sent to the client. This should be done programmatically using Rivet nodes or external scripts — not manually.

*Feel free to make any other changes you consider important.*

## Como executar
1. `python3 main.py`
2. O fluxo principal gera:
   * `app/monthly_report_albert.md`
   * `app/monthly_report_albert.pdf`
   * `app/monthly_report_summary.json`

Fluxo de simulação Rivet (reproduz prompts e artefatos):

```bash
# Rodar a simulação Rivet (gera logs, spec e output de relatório)
PYTHONPATH=. python3 rivet_workflow/simulated_rivet_workflow.py
```

### Arquivos principais
* `main.py` – entrada do fluxo de relatório.
* `app/report_workflow.py` – pipeline de cálculo, análise macro e geração de carta.
* `app/inputs/client_data.json` – dados de carteira e alocação do cliente Albert.
* `app/inputs/macro_data.json` – projeções macroeconômicas oficiais da XP.

### Resultados
- `app/monthly_report_albert.md` – carta mensal em português pronta para envio.
- `app/monthly_report_albert.pdf` – versão em PDF do relatório gerado automaticamente.
- `app/monthly_report_summary.json` – resumo JSON estruturado do relatório.
- `app/short_report.md` – resumo das melhorias, rationale e próximos passos.
- `rivet_workflow/rivet_simulation_spec.json` – especificação detalhada (nós, prompts, artefatos) da simulação Rivet.
- `rivet_workflow/rivet_simulated_output.pdf` – versão em PDF do relatório gerado pela simulação Rivet.
- `rivet_workflow/simulated_rivet_logs.json` – logs da execução simulada.

### Preparação Questions
In preparation for the meeting, prepare answers to the questions below:
* What are the main issues with the first version of the workflow?
* How did you decide on your approach to implementing the suggested changes?
* What else would you do if you had a full month to prepare this MVP?