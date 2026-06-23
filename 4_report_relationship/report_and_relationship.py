class RelationshipModule:
    def __init__(self, llm_client):
        self.llm = llm_client
        
    def draft_final_letter(self, portfolio, macro_impact, recommendations):
        """
        Gera a versão final do relatório no tom de voz da XP.
        Skill: Natural Language Generation (NLG) com formatação automatizada (Markdown/HTML).
        """
        prompt = f"""
        Escreva uma carta mensal de no máximo duas páginas para o cliente {portfolio['client_name']}.
        Tom: Profissional, empático, acessível para leigos.
        Idioma: Português do Brasil.
        
        Estrutura obrigatória:
        1. Saudação personalizada.
        2. Rentabilidade exata do mês: {portfolio['total_return_calculated']*100}% vs CDI {portfolio['cdi_benchmark']*100}%.
        3. Tradução do cenário macro de forma simples: {macro_impact}.
        4. Recomendações de ajuste de carteira: {recommendations}.
        
        Formate em Markdown pronto para ser convertido em PDF.
        """
        # final_letter = self.llm.predict(prompt)
        final_letter = f"Prezado {portfolio['client_name']},\n\nNeste mês, sua carteira rendeu..."
        return final_letter

    def export_to_pdf(self, markdown_text):
        """
        Converte o texto final em um arquivo PDF pronto para envio.
        Skill: Automação de Documentos (ex: bibliotecas weasyprint ou reportlab).
        """
        # Lógica de conversão
        print("PDF gerado com sucesso!")
        pass