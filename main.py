def main_workflow():
    # Inicialização (mocks de dependências)
    llm_client = "Fake_LLM_Client"
    
    # Execução sequencial dos nós (Nós do Rivet / Pipeline)
    quant = QuantModule("caminho/para/excel.xlsx")
    portfolio = quant.ingest_portfolio()
    portfolio = quant.calculate_metrics_vs_benchmark(portfolio)
    
    research = ResearchModule(llm_client)
    macro = research.analyze_macro_impact(portfolio)
    
    advisor = AdvisorModule(llm_client)
    recs = advisor.generate_recommendations(portfolio, macro)
    
    rel_module = RelationshipModule(llm_client)
    final_report = rel_module.draft_final_letter(portfolio, macro, recs)
    
    rel_module.export_to_pdf(final_report)
    return final_report

if __name__ == "__main__":
    main_workflow()