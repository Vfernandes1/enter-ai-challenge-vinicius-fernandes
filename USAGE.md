# AI Financial Advisor - Usage Guide

## Objetivo
Este projeto gera um relatório mensal em formato de carta para o cliente Albert da Silva, incluindo:
* desempenho da carteira,
* impacto macroeconômico,
* recomendações de ajuste compatíveis com o perfil de risco moderado e análise de pesquisa.

## Estrutura do Projeto
* `main.py` – executa o fluxo principal de geração do relatório.
* `app/report_workflow.py` – contém a lógica de ingestão de dados, cálculo de rentabilidade, análise macro, recomendações, geração de carta e exportação para Markdown/PDF/JSON.
* `app/inputs/client_data.json` – dados do portfólio e do cliente.
* `app/inputs/macro_data.json` – projeções macroeconômicas autorizadas pela XP.
* `rivet_workflow/` – contém a simulação do fluxo Rivet, logs e especificações de workflow.

## Como executar
1. Instale dependências Python (se necessário):
```bash
pip install reportlab
```

2. Execute o fluxo principal:
```bash
python3 main.py
```

3. O comando gerará automaticamente:
* `app/monthly_report_albert.md`
* `app/monthly_report_albert.pdf`
* `app/monthly_report_summary.json`

## Como executar a simulação Rivet
A simulação cria um fluxo de nós inspirado em Rivet, incluindo prompts e artefatos de cada etapa.

```bash
PYTHONPATH=. python3 rivet_workflow/simulated_rivet_workflow.py
```

Isso gera:
* `rivet_workflow/simulated_rivet_output.md`
* `rivet_workflow/simulated_rivet_output.pdf`
* `rivet_workflow/simulated_rivet_logs.json`
* `rivet_workflow/rivet_simulation_spec.json`
* `rivet_workflow/rivet_workflow_spec.yaml`

## O que foi automatizado
* Cálculo determinístico de rentabilidade ponderada da carteira.
* Avaliação de impacto macroeconômico com base nas diretrizes XP.
* Regras de recomendação alinhadas ao perfil moderado.
* Geração automática de carta em português com seções estruturadas.
* Exportação para Markdown, PDF e JSON.
* Simulação de workflow Rivet com registro de prompts e artefatos.

## Como usar esta solução
1. Atualize `app/inputs/client_data.json` com os dados reais do cliente.
2. Atualize `app/inputs/macro_data.json` com o cenário macro oficial.
3. Rode `python3 main.py` para gerar o relatório principal.
4. Use o JSON gerado em `app/monthly_report_summary.json` para integração com sistemas downstream.
5. Ajuste as regras de recomendação em `app/report_workflow.py` se desejar incorporar mais critérios quantitativos.

## Recomendação de próximos passos
* Conectar a entrada de dados ao Excel ou banco de dados real.
* Incluir um dashboard de visualização do desempenho mensal.
* Adicionar uma etapa de revisão e aprovação antes de emissão do PDF.
