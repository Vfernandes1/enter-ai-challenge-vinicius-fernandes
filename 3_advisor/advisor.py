class AdvisorModule:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.client_risk_profile = "Moderado: busca crescimento marginal, aceita risco médio, foco em dividendos e crédito BB+."
        
    def generate_recommendations(self, portfolio, macro_impact):
        """
        Gera sugestões de Compra/Venda/Manutenção baseadas em regras rígidas.
        Skill: Raciocínio Lógico Restrito (Chain of Thought focado em Perfil de Risco).
        """
        prompt = f"""
        Você é um Assessor Financeiro sênior. 
        Perfil do Cliente: {self.client_risk_profile}
        Alocação Atual: {portfolio['asset_allocation']}
        Impacto Macro: {macro_impact}
        
        Sua tarefa: Forneça recomendações de 'Compra', 'Venda' ou 'Manutenção' para os ativos.
        Regra de ouro: NUNCA recomende ativos de alto risco para um perfil moderado.
        """
        # Chamada ao LLM
        # recommendations = self.llm.predict(prompt)
        recommendations = "Sugerimos reduzir exposição em HAPV3 devido ao cenário de juros altos e alocar o capital em ativos atrelados ao CDI ou ações consolidadas de dividendos."
        return recommendations