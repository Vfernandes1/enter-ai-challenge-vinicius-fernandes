class ResearchModule:
    def __init__(self, llm_client):
        self.llm = llm_client # Instância do OpenAI/Anthropic/Gemini
        self.macro_context = """
        Economia em desaceleração. Selic projetada a 15,50%. IPCA em 6,1% para 2025. 
        Safra recorde de grãos impulsionará o PIB do 1º tri.
        """
        
    def analyze_macro_impact(self, portfolio):
        """
        Cruza a carteira do cliente com a análise macroeconômica.
        Skill: LLM Summarization & Entity Matching.
        """
        prompt = f"""
        Como analista macroeconômico, avalie como o seguinte cenário afeta esta carteira:
        Cenário: {self.macro_context}
        Carteira: {portfolio['assets']}
        
        Identifique riscos e oportunidades. Seja analítico e conciso.
        """
        # Chamada ao LLM
        # macro_impact = self.llm.predict(prompt)
        macro_impact = "A alta da Selic (15,50%) favorece fundos de renda fixa como Riza Lotus, mas penaliza o crédito de empresas na bolsa (como HAPV3 e LREN3)."
        return macro_impact