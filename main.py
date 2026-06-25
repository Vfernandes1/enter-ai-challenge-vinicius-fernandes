from app.report_workflow import PortfolioEngine
from pathlib import Path


def main_workflow():
    engine = PortfolioEngine(
        Path("app/inputs/client_data.json"),
        Path("app/inputs/macro_data.json")
    )
    engine.calculate_monthly_profitability()
    engine.evaluate_macro_impact()
    engine.generate_recommendations()
    engine.assess_risk_alignment()
    engine.build_letter()
    md_path = engine.export_markdown(Path("app/monthly_report_albert.md"))
    pdf_path = engine.export_pdf(Path("app/monthly_report_albert.pdf"))
    summary_path = engine.export_summary(Path("app/monthly_report_summary.json"))
    print(f"Relatório gerado em: {md_path}")
    print(f"PDF gerado em: {pdf_path}")
    print(f"Resumo JSON gerado em: {summary_path}")
    return md_path

if __name__ == "__main__":
    main_workflow()