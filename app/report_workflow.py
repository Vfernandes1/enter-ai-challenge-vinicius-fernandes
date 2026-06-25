import json
from pathlib import Path
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent

class PortfolioEngine:
    def __init__(self, client_data_path, macro_data_path):
        self.client_data_path = client_data_path
        self.macro_data_path = macro_data_path
        self.client_data = self._load_json(client_data_path)
        self.macro_data = self._load_json(macro_data_path)["xp_macro"]

    def _load_json(self, path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def calculate_monthly_profitability(self):
        holdings = self.client_data["holdings"]
        total_value = sum(item["current_value"] for item in holdings)
        weighted_returns = sum(item["current_value"] * item["reported_return"] for item in holdings)
        total_return = weighted_returns / total_value if total_value else 0.0

        class_returns = {}
        for item in holdings:
            classe = item["classe"]
            class_returns.setdefault(classe, {"value": 0.0, "weighted_return": 0.0})
            class_returns[classe]["value"] += item["current_value"]
            class_returns[classe]["weighted_return"] += item["current_value"] * item["reported_return"]

        for classe, data in class_returns.items():
            data["share"] = data["value"] / total_value if total_value else 0.0
            data["return"] = data["weighted_return"] / data["value"] if data["value"] else 0.0

        self.client_data["portfolio_value"] = total_value
        self.client_data["monthly_return"] = total_return
        self.client_data["class_returns"] = class_returns
        self.client_data["benchmark_cdi"] = 0.037
        self.client_data["benchmark_ipca"] = self.macro_data["cpi_2025"] / 100
        return self.client_data

    def evaluate_macro_impact(self):
        macro = self.macro_data
        holdings = self.client_data["holdings"]
        risks = []
        opportunities = []

        if macro["selic_terminal_2025"] >= 15.0:
            opportunities.append("A taxa Selic alta fortalece a renda fixa de qualidade e pressiona o crédito corporativo mais arriscado.")
            risks.append("Ativos de renda variável com alavancagem ou que dependem de redução de juros podem sofrer volatilidade adicional.")

        if macro["pib_2025"] <= 2.0:
            risks.append("O crescimento econômico moderado reduz o apetite por risco e pode limitar a recuperação de ações cíclicas.")

        if macro["usd_2025"] >= 6.0:
            opportunities.append("Empresas com receitas em dólar ou fluxos de exportação podem se beneficiar do câmbio mais elevado.")

        high_risk_names = [x["ticker"] for x in holdings if x["classe"] == "Ações" and x["reported_return"] < -0.20]
        if high_risk_names:
            risks.append(f"Posições de ações mais voláteis como {', '.join(high_risk_names)} exigem atenção extra em um cenário de juros altos.")

        self.client_data["macro_impact"] = {
            "summary": "O cenário XP indica juros elevados, inflação persistente e crescimento econômico moderado.",
            "risks": risks,
            "opportunities": opportunities,
            "official_projection": macro
        }
        return self.client_data["macro_impact"]

    def generate_recommendations(self):
        profile = self.client_data["risk_profile"]
        holdings = self.client_data["holdings"]
        recommendations = []
        allocate_to_fixed_income = self.client_data["class_returns"]["Renda Fixa"]["share"] < 0.15

        recommendations.append("Manter a alocação principal em fundos e renda fixa, ajustando posições de maior risco em ações.")

        for item in holdings:
            if item["classe"] == "Ações":
                if item["reported_return"] < -0.30:
                    recommendations.append(f"Considerar reduzir exposição em {item['ticker']} ({item['name']}) por seu desempenho fraco e maior volatilidade.")
                elif item["reported_return"] > 0.20 and item["ticker"] == "MRFG3":
                    recommendations.append("Aproveitar parte da alta de MRFG3 para rebalancear e preservar ganhos, mantendo exposição moderada.")

        if allocate_to_fixed_income:
            recommendations.append("Reforçar a exposição em renda fixa de alta qualidade, especialmente títulos indexados ao CDI ou crédito com rating BB+ ou superior.")

        recommendations.append("Evitar alterações bruscas de curto prazo e focar no médio prazo, como exige o perfil moderado.")
        self.client_data["recommendations"] = recommendations
        return recommendations

    def assess_risk_alignment(self):
        target = {
            "Ações": 0.20,
            "Fundos": 0.65,
            "Renda Fixa": 0.15
        }
        actual = self.client_data["class_returns"]
        deviation = 0.0
        details = []
        for classe, target_share in target.items():
            actual_share = actual.get(classe, {}).get("share", 0.0)
            diff = actual_share - target_share
            deviation += abs(diff)
            if diff > 0.05:
                details.append(f"Excesso de {classe}: {actual_share*100:.1f}% vs alvo {target_share*100:.0f}%.")
            elif diff < -0.05:
                details.append(f"Subexposição em {classe}: {actual_share*100:.1f}% vs alvo {target_share*100:.0f}%.")

        score = max(0, 100 - deviation * 100)
        if score >= 80:
            note = "A alocação está consistentemente alinhada com um perfil moderado."
        elif score >= 60:
            note = "A alocação está parcialmente alinhada, com alguns desvios que podem ser ajustados gradualmente."
        else:
            note = "A carteira apresenta desvios relevantes em relação ao perfil moderado e merece rebalanceamento cuidadoso."

        self.client_data["risk_alignment"] = {
            "score": round(score, 1),
            "note": note,
            "details": details
        }
        return self.client_data["risk_alignment"]

    def build_letter(self):
        data = self.client_data
        date_str = date.today().strftime("%d/%m/%Y")
        monthly_pct = data["monthly_return"] * 100
        cdi_pct = data["benchmark_cdi"] * 100
        ipca_pct = data["benchmark_ipca"] * 100

        sections = [
            f"São Paulo, {date_str}",
            "",
            f"Prezado Sr. {data['client_name']},",
            "",
            "Segue o relatório mensal da sua carteira. Nosso objetivo é traduzir o desempenho e os impactos macroeconômicos em decisões práticas para o seu perfil moderado.",
            "",
            "1. Desempenho da carteira",
            f"Sua carteira apresentou uma rentabilidade estimada de {monthly_pct:.2f}% no último mês, contra um CDI de {cdi_pct:.2f}% e inflação referência de {ipca_pct:.2f}%.",
            f"O valor de mercado estimado da carteira é de R$ {data['portfolio_value']:.2f}.",
            "",
            "Desempenho por classe de ativo:",
        ]

        for classe, class_data in data["class_returns"].items():
            sections.append(f"- {classe}: {class_data['share']*100:.1f}% da carteira com retorno médio de {class_data['return']*100:.2f}%.")

        best_holdings = sorted(data["holdings"], key=lambda item: item["reported_return"])[-2:]
        worst_holdings = sorted(data["holdings"], key=lambda item: item["reported_return"])[:2]
        sections += [
            "",
            "Principais contribuições ao desempenho:",
        ]
        for item in reversed(best_holdings):
            sections.append(f"- {item['ticker']} ({item['name']}): retorno de {item['reported_return']*100:.2f}%.")
        for item in worst_holdings:
            sections.append(f"- {item['ticker']} ({item['name']}): retorno de {item['reported_return']*100:.2f}%.")

        sections += [
            "",
            "2. Como o cenário macro impacta sua carteira",
            f"O cenário XP aponta Selic em 15,50%, IPCA em 6,1% e câmbio projetado de R$ 6,20 para 2025.",
            f"Resumo: {data['macro_impact']['summary']}",
        ]

        if data['macro_impact']['opportunities']:
            sections.append("Oportunidades identificadas:")
            for opp in data['macro_impact']['opportunities']:
                sections.append(f"- {opp}")

        if data['macro_impact']['risks']:
            sections.append("Riscos relevantes:")
            for risk in data['macro_impact']['risks']:
                sections.append(f"- {risk}")

        sections += [
            "",
            "3. Ajustes recomendados para o seu perfil",
            "Com base no perfil moderado, o foco é estabilidade e preservação do poder de compra, sem abrir mão de crescimento moderado.",
        ]

        for rec in data['recommendations']:
            sections.append(f"- {rec}")

        sections += [
            "",
            "4. Avaliação de alinhamento com o perfil de risco",
            f"Score de alinhamento: {data['risk_alignment']['score']:.1f}/100.",
            data['risk_alignment']['note'],
            "",
            "4. Observações finais",
            "Recomendamos revisar essas posições no próximo ciclo mensal e validar quaisquer movimentações com seu assessor antes de executar ordens.",
            "",
            "Atenciosamente,",
            "Vinícius F.",
            "Assessor Financeiro XP"
        ]

        self.client_data["final_letter"] = "\n".join(sections)
        return self.client_data["final_letter"]

    def export_markdown(self, output_path):
        if "final_letter" not in self.client_data:
            self.build_letter()
        content = self.client_data["final_letter"]
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    def export_pdf(self, output_path):
        if "final_letter" not in self.client_data:
            self.build_letter()
        text = self.client_data["final_letter"]
        c = canvas.Canvas(str(output_path), pagesize=A4)
        width, height = A4
        margin = 20 * mm
        y = height - margin
        line_height = 12
        max_chars = 95

        for paragraph in text.split("\n"):
            if not paragraph.strip():
                y -= line_height
                continue
            if paragraph.startswith("- "):
                c.setFont("Helvetica", 11)
                c.drawString(margin + 8 * mm, y, u"• " + paragraph[2:])
                y -= line_height
            else:
                c.setFont("Helvetica", 11)
                while paragraph:
                    chunk = paragraph[:max_chars]
                    c.drawString(margin, y, chunk)
                    paragraph = paragraph[max_chars:]
                    y -= line_height
            if y < margin + 40:
                c.showPage()
                y = height - margin
        c.save()
        return output_path

    def export_summary(self, output_path):
        if "final_letter" not in self.client_data:
            self.build_letter()
        summary = {
            "client_name": self.client_data["client_name"],
            "portfolio_value": self.client_data["portfolio_value"],
            "monthly_return": self.client_data["monthly_return"],
            "benchmark_cdi": self.client_data["benchmark_cdi"],
            "benchmark_ipca": self.client_data["benchmark_ipca"],
            "class_returns": self.client_data["class_returns"],
            "risk_alignment": self.client_data["risk_alignment"],
            "macro_impact": self.client_data["macro_impact"],
            "recommendations": self.client_data["recommendations"],
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        return output_path

    def export_csv(self, output_path):
        """Export class breakdown and top holdings to CSV for downstream systems."""
        import csv

        if "class_returns" not in self.client_data:
            self.calculate_monthly_profitability()

        class_rows = []
        for classe, data in self.client_data["class_returns"].items():
            class_rows.append({
                "class": classe,
                "share": data.get("share", 0.0),
                "return": data.get("return", 0.0),
                "value": data.get("value", 0.0),
            })

        top_holdings = sorted(self.client_data.get("holdings", []), key=lambda x: x.get("current_value", 0), reverse=True)[:10]

        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["section", "key", "name", "value", "metric"])
            for r in class_rows:
                writer.writerow(["class_breakdown", r["class"], "", f"{r['value']:.2f}", f"share={r['share']:.4f};return={r['return']:.4f}"])

            writer.writerow(["", "", "", "", ""])
            writer.writerow(["top_holding", "ticker", "name", "current_value", "reported_return"])
            for h in top_holdings:
                writer.writerow(["top_holding", h.get("ticker"), h.get("name"), f"{h.get('current_value',0):.2f}", f"{h.get('reported_return',0):.4f}"])

        return output_path


if __name__ == "__main__":
    engine = PortfolioEngine(BASE_DIR / "inputs" / "client_data.json", BASE_DIR / "inputs" / "macro_data.json")
    engine.calculate_monthly_profitability()
    engine.evaluate_macro_impact()
    engine.generate_recommendations()
    engine.build_letter()
    markdown_output = engine.export_markdown(BASE_DIR / "monthly_report_albert.md")
    pdf_output = engine.export_pdf(BASE_DIR / "monthly_report_albert.pdf")
    summary_output = engine.export_summary(BASE_DIR / "monthly_report_summary.json")
    print(f"Relatório gerado em: {markdown_output}")
    print(f"PDF gerado em: {pdf_output}")
    print(f"Resumo JSON gerado em: {summary_output}")
