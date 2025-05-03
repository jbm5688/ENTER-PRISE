import random
import logging
from datetime import datetime, timedelta

logger = logging.getLogger("franquia_finder")

class MarketResearchCollector:
    """
    Classe responsável por coletar dados de pesquisas de mercado.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o coletor de pesquisa de mercado.
        
        Args:
            config (dict): Configurações para coleta de dados
        """
        self.config = config or {}
    
    def collect_research_data(self, categories=None, days=90):
        """
        Coleta dados de pesquisa de mercado (versão simulada para testes).
        
        Args:
            categories (list): Lista de categorias para filtrar
            days (int): Número de dias para análise
            
        Returns:
            list: Lista de dados de pesquisa de mercado
        """
        print("Simulando coleta de dados de pesquisa de mercado...")
        
        # Categorias padrão se não forem fornecidas
        if not categories:
            categories = [
                "Alimentação", "Saúde", "Educação", "Tecnologia", 
                "Pet", "Moda", "Beleza", "Serviços", "Varejo", "Casa"
            ]
        
        # Data base para simulação
        base_date = datetime.now()
        
        # Gerar dados simulados
        research_data = []
        
        for category in categories:
            # Gerar entre 2 e 5 relatórios por categoria
            num_reports = random.randint(2, 5)
            
            for i in range(num_reports):
                # Gerar data do relatório (nos últimos "days" dias)
                report_date = base_date - timedelta(days=random.randint(1, days))
                
                # Títulos simulados de relatórios
                titles = [
                    f"Análise de Mercado: {category}",
                    f"Tendências do Setor de {category}",
                    f"Oportunidades em {category}",
                    f"Pesquisa de Consumidor: {category}",
                    f"Relatório de Investimento: {category}"
                ]
                
                # Selecionar um título aleatoriamente
                title = random.choice(titles)
                
                # Gerar métricas simuladas
                market_size = random.randint(100, 1000) * 1000000  # Em milhões
                growth_rate = random.uniform(0.02, 0.25)  # 2% a 25%
                consumer_satisfaction = random.uniform(0.5, 0.95)  # 50% a 95%
                investment_opportunity = random.uniform(0.3, 0.9)  # 30% a 90%
                
                # Gerar fontes simuladas
                sources = [
                    "Associação Brasileira de Franchising",
                    "IBGE",
                    "Sebrae",
                    "Consultoria McKinsey",
                    "Kantar Worldpanel",
                    "Nielsen",
                    "Euromonitor International",
                    "Fundação Getúlio Vargas"
                ]
                
                # Selecionar uma fonte aleatoriamente
                source = random.choice(sources)
                
                # Gerar insights de mercado simulados
                insights = [
                    f"O mercado de {category} deve crescer {growth_rate*100:.1f}% nos próximos 2 anos",
                    f"Consumidores valorizam qualidade e preço no setor de {category}",
                    f"Novas tecnologias estão transformando o setor de {category}",
                    f"Franquias de {category} têm mostrado resistência em períodos de crise",
                    f"O segmento online em {category} tem crescido acima da média do mercado",
                    f"Há uma tendência de consolidação no setor de {category}",
                    f"Empresas com foco em sustentabilidade têm se destacado em {category}"
                ]
                
                # Selecionar 2-3 insights aleatoriamente
                selected_insights = random.sample(insights, random.randint(2, 3))
                
                # Critérios de sucesso simulados
                success_criteria = [
                    "Localização estratégica",
                    "Atendimento de qualidade",
                    "Marketing digital eficiente",
                    "Gestão de custos",
                    "Inovação constante",
                    "Treinamento da equipe",
                    "Experiência do cliente",
                    "Precificação competitiva"
                ]
                
                # Selecionar 2-4 critérios aleatoriamente
                selected_criteria = random.sample(success_criteria, random.randint(2, 4))
                
                # Criar relatório simulado
                report = {
                    "title": title,
                    "category": category,
                    "date": report_date.strftime('%Y-%m-%d'),
                    "source": source,
                    "market_size": market_size,
                    "growth_rate": growth_rate,
                    "consumer_satisfaction": consumer_satisfaction,
                    "investment_opportunity": investment_opportunity,
                    "insights": selected_insights,
                    "success_criteria": selected_criteria,
                    "keywords": [category.lower(), "franquia", "oportunidade", "mercado"]
                }
                
                research_data.append(report)
        
        logger.info(f"Coletados {len(research_data)} relatórios de pesquisa de mercado simulados")
        return research_data
